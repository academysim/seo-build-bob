# -*- coding: utf-8 -*-
"""Daily Search Console snapshot and regression-first diff, across every property.

READ ONLY. This tool never writes to a site directory, never deploys and never
edits a page. It reads the Search Console API and writes JSON snapshots plus a
report. That is deliberate: the thing it replaces (an agentic SEO skill whose
daily runner is `claude -p --permission-mode acceptEdits`) edits the repo
unattended, and three deploys have already reverted the booking money path.

Why it exists: organic search fell about 70% in the week of 2026-08-10 and
bookings followed roughly two weeks later. It was found from the bookings. A
daily snapshot with a period-over-period diff is the instrument that sees it in
the first week instead of the third.

## Windows, and why they are not day over day

Search Console data lags two to three days and backfills. A day-over-day diff on
fresh data mostly measures the backfill. So the diff compares the last COMPLETE
7 days against the 7 before them, both ending at the lag boundary. That is
stable enough to act on and still catches a step change inside a week.

## Auth

Two ways, whichever credential is present:

  service account   GSC_SERVICE_ACCOUNT=<path to key.json>, and the service
                    account's email added as a user on each property in Search
                    Console. Best for an unattended schedule: nothing expires.

  OAuth             `python gsc_monitor.py auth` once, in a browser. Uses the
                    web client already on this box. The refresh token lands in
                    .gsc/token.json (gitignored).

    !! If the OAuth consent screen is still in "Testing", Google expires the
       refresh token after 7 DAYS and the daily run dies silently. Either publish
       the app (APIs & Services > OAuth consent screen > Publish) or use a
       service account. `sites` prints a warning when the token is near that age.

## Usage

  python gsc_monitor.py auth              one-time browser consent
  python gsc_monitor.py sites             list verified properties
  python gsc_monitor.py pull              snapshot every property, then report
  python gsc_monitor.py pull --days 28    change the window
  python gsc_monitor.py report            re-print from the last two snapshots
"""
import base64
import datetime as dt
import glob
import io
import json
import os
import sys
import time
import urllib.parse

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SECRETS = os.path.join(ROOT, '.gsc')
SNAPS = os.path.join(ROOT, 'analytics', 'gsc')
TOKEN = os.path.join(SECRETS, 'token.json')

API = 'https://searchconsole.googleapis.com/webmasters/v3'
SCOPE = 'https://www.googleapis.com/auth/webmasters'  # full scope so `submit` can PUT sitemaps; re-run `auth` after changing
REDIRECT = 'http://localhost:8910/callback'

# Search Console finalises data on a lag. Everything inside this many days of
# today is still moving, so no window ever includes it.
LAG_DAYS = 3
ROW_LIMIT = 500


def out(s=''):
    """Print UTF-8 on a cp1252 console without dying on a single character."""
    sys.stdout.flush()
    sys.stdout.buffer.write((s + '\n').encode('utf-8', 'replace'))
    sys.stdout.buffer.flush()


# ---------------------------------------------------------------- credentials

def client_config():
    """The OAuth web client. Downloads first, then .gsc/, then GSC_CLIENT_SECRET."""
    cands = []
    env = os.environ.get('GSC_CLIENT_SECRET')
    if env:
        cands.append(env)
    cands += sorted(glob.glob(os.path.join(SECRETS, 'client_secret*.json')))
    cands += sorted(glob.glob(os.path.join(
        os.path.expanduser('~'), 'Downloads', 'client_secret*.json')))
    for f in cands:
        if os.path.exists(f):
            d = json.load(io.open(f, encoding='utf-8'))
            for kind in ('web', 'installed'):
                if kind in d:
                    return d[kind], f
    raise SystemExit(
        '  !! no OAuth client JSON found.\n'
        '     Looked in $GSC_CLIENT_SECRET, .gsc/ and ~/Downloads/.\n'
        '     Or set GSC_SERVICE_ACCOUNT to a service-account key instead.')


def sa_token():
    """Self-signed JWT -> access token. No google SDK, just PyJWT."""
    path = os.environ.get('GSC_SERVICE_ACCOUNT')
    if not path or not os.path.exists(path):
        return None
    import jwt  # PyJWT
    key = json.load(io.open(path, encoding='utf-8'))
    now = int(time.time())
    claim = {
        'iss': key['client_email'],
        'scope': SCOPE,
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': now,
        'exp': now + 3600,
    }
    assertion = jwt.encode(claim, key['private_key'], algorithm='RS256')
    r = requests.post('https://oauth2.googleapis.com/token', timeout=30, data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': assertion})
    if r.status_code != 200:
        raise SystemExit('  !! service account rejected: %s %s' % (r.status_code, r.text[:300]))
    return r.json()['access_token']


def do_auth():
    """One-time consent. Spins a loopback server on the client's redirect port."""
    import http.server
    import threading
    import webbrowser

    cfg, src = client_config()
    out('  client from %s' % src)
    state = base64.urlsafe_b64encode(os.urandom(18)).decode().rstrip('=')
    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode({
        'client_id': cfg['client_id'],
        'redirect_uri': REDIRECT,
        'response_type': 'code',
        'scope': SCOPE,
        'access_type': 'offline',
        'prompt': 'consent',          # forces a refresh_token even on re-auth
        'state': state,
    })

    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            if q.get('state', [''])[0] != state:
                self.wfile.write(b'<h3>State mismatch. Close this and retry.</h3>')
                return
            if 'code' in q:
                got['code'] = q['code'][0]
                self.wfile.write(b'<h3>Authorised. You can close this tab.</h3>')
            else:
                got['error'] = q.get('error', ['unknown'])[0]
                self.wfile.write(b'<h3>Denied. You can close this tab.</h3>')

    srv = http.server.HTTPServer(('localhost', 8910), H)
    threading.Thread(target=srv.handle_request, daemon=True).start()
    out('\n  Opening a browser. If nothing opens, paste this:\n')
    out('  ' + url + '\n')
    try:
        webbrowser.open(url)
    except Exception:
        pass
    for _ in range(300):
        if got:
            break
        time.sleep(1)
    srv.server_close()
    if 'code' not in got:
        raise SystemExit('  !! no authorisation code (%s)' % got.get('error', 'timed out'))

    r = requests.post('https://oauth2.googleapis.com/token', timeout=30, data={
        'code': got['code'], 'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret'], 'redirect_uri': REDIRECT,
        'grant_type': 'authorization_code'})
    if r.status_code != 200:
        raise SystemExit('  !! token exchange failed: %s %s' % (r.status_code, r.text[:300]))
    tok = r.json()
    if 'refresh_token' not in tok:
        raise SystemExit('  !! Google returned no refresh_token. Revoke this app at '
                         'myaccount.google.com/permissions and run auth again.')
    if not os.path.isdir(SECRETS):
        os.makedirs(SECRETS)
    tok['obtained'] = dt.datetime.now(dt.timezone.utc).isoformat()
    io.open(TOKEN, 'w', encoding='utf-8').write(json.dumps(tok, indent=2))
    ensure_gitignore()
    out('  refresh token stored in .gsc/token.json (gitignored)')
    out('  now run:  python gsc_monitor.py sites')


def access_token():
    t = sa_token()
    if t:
        return t, 'service-account'
    if not os.path.exists(TOKEN):
        raise SystemExit('  !! not authorised yet. Run: python gsc_monitor.py auth')
    cfg, _ = client_config()
    tok = json.load(io.open(TOKEN, encoding='utf-8'))
    r = requests.post('https://oauth2.googleapis.com/token', timeout=30, data={
        'refresh_token': tok['refresh_token'], 'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret'], 'grant_type': 'refresh_token'})
    if r.status_code != 200:
        raise SystemExit(
            '  !! refresh failed: %s %s\n'
            '     If this says invalid_grant, the consent screen is probably still in\n'
            '     "Testing" and Google expired the token after 7 days. Publish the app\n'
            '     or switch to a service account, then run auth again.'
            % (r.status_code, r.text[:200]))
    return r.json()['access_token'], 'oauth'


def ensure_gitignore():
    gi = os.path.join(ROOT, '.gitignore')
    cur = io.open(gi, encoding='utf-8').read() if os.path.exists(gi) else ''
    if '.gsc/' not in cur:
        io.open(gi, 'a', encoding='utf-8', newline='\n').write(
            '\n# Search Console credentials - never commit\n.gsc/\n')


# ------------------------------------------------------------------- fetching

def api(tok, path, body=None):
    url = '%s/%s' % (API, path)
    h = {'Authorization': 'Bearer ' + tok}
    for attempt in range(4):
        if body is None:
            r = requests.get(url, headers=h, timeout=60)
        else:
            r = requests.post(url, headers=h, json=body, timeout=60)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 503):
            time.sleep(2 ** attempt)
            continue
        return {'_error': '%s %s' % (r.status_code, r.text[:240])}
    return {'_error': 'gave up after retries'}


def list_sites(tok):
    d = api(tok, 'sites')
    if '_error' in d:
        raise SystemExit('  !! %s' % d['_error'])
    rows = d.get('siteEntry', [])
    keep = [s for s in rows
            if s.get('permissionLevel') != 'siteUnverifiedUser'
            and 'academysim' in s.get('siteUrl', '')]
    return keep, rows


def window(days, offset=0):
    end = dt.date.today() - dt.timedelta(days=LAG_DAYS + offset)
    start = end - dt.timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def query(tok, site, start, end, dims):
    body = {'startDate': start, 'endDate': end, 'rowLimit': ROW_LIMIT,
            'dataState': 'final'}
    if dims:
        body['dimensions'] = dims
    d = api(tok, 'sites/%s/searchAnalytics/query' % urllib.parse.quote(site, safe=''), body)
    if '_error' in d:
        return None, d['_error']
    return d.get('rows', []), None


def pull(days=7):
    tok, how = access_token()
    sites, allrows = list_sites(tok)
    if not sites:
        raise SystemExit('  !! no verified academysim properties on this account (%d total)'
                         % len(allrows))
    cs, ce = window(days, 0)
    ps, pe = window(days, days)
    out('  auth %s | %d properties | current %s..%s | prior %s..%s'
        % (how, len(sites), cs, ce, ps, pe))

    snap = {'generated': dt.datetime.now(dt.timezone.utc).isoformat(),
            'window_days': days, 'current': [cs, ce], 'prior': [ps, pe],
            'lag_days': LAG_DAYS, 'properties': {}}

    for s in sites:
        site = s['siteUrl']
        rec = {'permission': s.get('permissionLevel')}
        for label, (a, b) in (('current', (cs, ce)), ('prior', (ps, pe))):
            block = {}
            for name, dims in (('totals', []), ('query', ['query']), ('page', ['page'])):
                rows, err = query(tok, site, a, b, dims)
                if err:
                    block[name] = {'_error': err}
                else:
                    block[name] = rows
            rec[label] = block
        snap['properties'][site] = rec
        t = rec['current'].get('totals')
        if isinstance(t, list) and t:
            out('    %-42s %5d clicks  %7d impr' % (site, t[0]['clicks'], t[0]['impressions']))
        elif isinstance(t, dict) and '_error' in t:
            out('    %-42s !! %s' % (site, t['_error'][:70]))
        else:
            out('    %-42s no data returned' % site)

    if not os.path.isdir(SNAPS):
        os.makedirs(SNAPS)
    p = os.path.join(SNAPS, '%s.json' % dt.date.today().isoformat())
    io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(snap, indent=1))
    out('\n  snapshot -> %s' % os.path.relpath(p, ROOT))
    return snap


# -------------------------------------------------------------------- report

def index(rows, key):
    if not isinstance(rows, list):
        return None                      # an error block: missing, not empty
    return {r['keys'][0]: r for r in rows if r.get('keys')}


def totals_of(block):
    t = block.get('totals')
    if isinstance(t, list) and t:
        return t[0]
    return None


def report(snap):
    days = snap['window_days']
    out('')
    out('=' * 78)
    out('  SEARCH CONSOLE, last %d days vs the %d before' % (days, days))
    out('  current %s..%s   prior %s..%s   (data lag %d days)'
        % (tuple(snap['current']) + tuple(snap['prior']) + (snap['lag_days'],)))
    out('=' * 78)

    out('')
    out('  PROPERTY TOTALS')
    out('  %-40s %8s %8s %9s %7s' % ('', 'clicks', 'was', 'change', 'pos'))
    hits = []
    for site, rec in sorted(snap['properties'].items()):
        c, p = totals_of(rec['current']), totals_of(rec['prior'])
        if c is None:
            out('  %-40s   no data returned for the current window' % site)
            continue
        was = p['clicks'] if p else None
        if was is None:
            out('  %-40s %8d %8s %9s %7.1f'
                % (site, c['clicks'], 'n/a', 'n/a', c['position']))
            continue
        d = c['clicks'] - was
        pct = (d / was * 100.0) if was else None
        out('  %-40s %8d %8d %+8s %7.1f'
            % (site, c['clicks'], was,
               ('%+.0f%%' % pct) if pct is not None else '%+d' % d, c['position']))
        if was >= 5 and pct is not None and pct <= -25:
            hits.append((pct, site, was, c['clicks']))

    if hits:
        out('')
        out('  !! PROPERTY-LEVEL DROP, 25% or worse on a base of 5+ clicks')
        for pct, site, was, now in sorted(hits):
            out('     %-40s %d -> %d clicks  (%+.0f%%)' % (site, was, now, pct))

    # ---- regressions, the section that exists to be read first
    out('')
    out('  REGRESSIONS, biggest click losses by query')
    any_reg = False
    for site, rec in sorted(snap['properties'].items()):
        cq, pq = index(rec['current'].get('query'), 'query'), index(rec['prior'].get('query'), 'query')
        if cq is None or pq is None:
            continue
        losses = []
        for k, pr in pq.items():
            now = cq.get(k, {}).get('clicks', 0)
            if pr['clicks'] - now >= 2:
                losses.append((now - pr['clicks'], k, pr, cq.get(k)))
        for d, k, pr, cur in sorted(losses)[:6]:
            any_reg = True
            pos = ('%.1f -> %.1f' % (pr['position'], cur['position'])) if cur else 'gone from top %d' % ROW_LIMIT
            out('     %-26s %+3d clicks (%d -> %d)  pos %s'
                % (k[:26], d, pr['clicks'], cur['clicks'] if cur else 0, pos))
    if not any_reg:
        out('     none at or above a 2-click loss')

    # ---- quick wins
    out('')
    out('  QUICK WINS, positions 4 to 15 with impressions and few clicks')
    wins = []
    for site, rec in sorted(snap['properties'].items()):
        rows = rec['current'].get('query')
        if not isinstance(rows, list):
            continue
        for r in rows:
            if 4 <= r['position'] <= 15 and r['impressions'] >= 30:
                wins.append((-r['impressions'], r['keys'][0], r))
    for _, k, r in sorted(wins)[:10]:
        out('     %-30s pos %5.1f  %6d impr  %3d clicks  ctr %.1f%%'
            % (k[:30], r['position'], r['impressions'], r['clicks'], r['ctr'] * 100))
    if not wins:
        out('     none')

    # ---- pages losing clicks
    out('')
    out('  PAGES LOSING CLICKS')
    shown = 0
    for site, rec in sorted(snap['properties'].items()):
        cp, pp = index(rec['current'].get('page'), 'page'), index(rec['prior'].get('page'), 'page')
        if cp is None or pp is None:
            continue
        for k, pr in pp.items():
            now = cp.get(k, {}).get('clicks', 0)
            if pr['clicks'] - now >= 3:
                out('     %-58s %d -> %d' % (k[-58:], pr['clicks'], now))
                shown += 1
    if not shown:
        out('     none at or above a 3-click loss')

    out('')
    out('  Nothing above was written to any site file. This tool is read only.')
    out('')


def load_latest():
    fs = sorted(glob.glob(os.path.join(SNAPS, '*.json')))
    if not fs:
        raise SystemExit('  !! no snapshots yet. Run: python gsc_monitor.py pull')
    return json.load(io.open(fs[-1], encoding='utf-8'))


SITEMAPS = {
    'sc-domain:academysim.com': ['https://academysim.com/sitemap.xml', 'https://lounge.academysim.com/sitemap.xml',
        'https://events.academysim.com/sitemap.xml', 'https://builds.academysim.com/sitemap.xml',
        'https://driver.academysim.com/sitemap.xml', 'https://health.academysim.com/sitemap.xml'],
}


def submit_sitemaps():
    """PUT every sitemap in SITEMAPS to Search Console (needs the full webmasters scope)."""
    tok, how = access_token()
    for site, urls in SITEMAPS.items():
        for u in urls:
            path = 'sites/%s/sitemaps/%s' % (urllib.parse.quote(site, safe=''), urllib.parse.quote(u, safe=''))
            r = requests.put('%s/%s' % (API, path), headers={'Authorization': 'Bearer ' + tok}, timeout=60)
            out('  %-55s %s' % (u, 'submitted' if r.status_code in (200, 204) else '!! %s %s' % (r.status_code, r.text[:120])))
        d = api(tok, 'sites/%s/sitemaps' % urllib.parse.quote(site, safe=''))
        for sm in d.get('sitemap', []):
            out('    %-55s last submitted %s  errors %s' % (sm.get('path'), (sm.get('lastSubmitted') or '')[:10], sm.get('errors')))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'pull'
    if cmd == 'auth':
        return do_auth()
    if cmd == 'submit':
        return submit_sitemaps()
    if cmd == 'sites':
        tok, how = access_token()
        keep, allrows = list_sites(tok)
        out('  auth %s' % how)
        out('  %d properties on the account, %d are academysim:' % (len(allrows), len(keep)))
        for s in allrows:
            mark = '  *' if s in keep else '   '
            out('   %s %-46s %s' % (mark, s['siteUrl'], s.get('permissionLevel')))
        if how == 'oauth' and os.path.exists(TOKEN):
            t = json.load(io.open(TOKEN, encoding='utf-8'))
            if t.get('obtained'):
                age = (dt.datetime.now(dt.timezone.utc)
                       - dt.datetime.fromisoformat(t['obtained'])).days
                out('\n  refresh token is %d days old.' % age)
                if age >= 5:
                    out('  !! If the consent screen is still in "Testing", Google expires it')
                    out('     at 7 days. Publish the app or move to a service account.')
        return
    if cmd == 'report':
        return report(load_latest())
    if cmd == 'pull':
        days = 7
        if '--days' in sys.argv:
            days = int(sys.argv[sys.argv.index('--days') + 1])
        return report(pull(days))
    raise SystemExit(__doc__)


if __name__ == '__main__':
    main()

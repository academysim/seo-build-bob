# -*- coding: utf-8 -*-
"""Generate llms.txt for every property, from the sitemap and the staged pages.

Why this exists: every subdomain returns 404 on /llms.txt, so the one file an AI
crawler looks for to understand a site is missing on all six. The main store has
one, but Shopify generates it and it is about Shop Pay and checkout - it says
nothing about the lounge, driver education or the senior programs.

The URL list comes from site/sitemap.xml, which is the truth about what is live.
Titles and descriptions come from the staged HTML, so they are the same strings
that already passed each property's audit. Nothing here is authored twice.

The FACTS block per property is the point. It is the one place an assistant reads
before answering a question about Academy, so the disclosures that our audits
enforce on every page are repeated there verbatim: no simulators installed in any
Florida school district, not a state-licensed driver-education provider, not a
medical provider, not affiliated with any racing series.

Order matters: run this AFTER stage.py, because it prefers upload/ and upload/ is
cleared and repopulated by build_all.py on every run.

Usage: python gen_llms.py [key ...]        (default: all five)
"""
import io, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)
from shared.tools.constants import HOSTS

# The em dash transform is lounge/tools/strip_dashes.py's, kept identical on
# purpose: llms.txt is authored copy and the house rule applies to it too.
EMDASH = re.compile(r'\s*(?:&mdash;|—)\s*')

SITES = {
    'lounge': dict(
        name='Academy Sim Racing, Sim Racing Lounge (Tampa)',
        facts=[
            'A walk-in sim racing lounge in Tampa, Florida. Sessions are booked per rig, '
            'not per person.',
            'The rigs run iRacing and Assetto Corsa. No car in the lounge is a real vehicle '
            'and no session takes place on a public road.',
        ],
    ),
    'events': dict(
        name='Academy Sim Racing, Event Simulator Rentals',
        facts=[
            'Racing simulators rented with staff for corporate events, trade shows, '
            'dealership activations and private parties, in Tampa and statewide Florida.',
            'Academy Sim Racing is not affiliated with, endorsed by or licensed by Formula 1, '
            'NASCAR, IMSA or any racing series, sanctioning body or vehicle manufacturer.',
            'City and location pages describe where Academy travels to work. They are not '
            'branch offices and Academy has no premises in those cities.',
        ],
    ),
    'builds': dict(
        name='Academy Sim Racing, Custom Simulator Builds',
        facts=[
            'Custom racing simulators built to order and shipped or installed.',
            'Five builds are published, priced from $7,495 to $39,995. Any price quoted '
            'outside those five is not a published price.',
            'Most builds are configured in a consultation rather than bought off the page.',
            'Pages named after a circuit describe a build placed NEAR that circuit at an '
            'independent business. Academy Sim Racing is not affiliated with, endorsed by or '
            'partnered with any racetrack and operates no branch at any circuit.',
        ],
    ),
    'driver': dict(
        name="Academy Driver's Ed, Driving Simulator Training",
        facts=[
            'Driving simulator training for teens, plus simulator rentals and systems for '
            'schools, driver-education programs and public-safety organizations.',
            'Academy Sim Racing does not currently have simulators installed in Florida '
            'school districts. Pages describing district programs describe services Academy '
            'offers and can deploy, not installations that exist.',
            'Academy Sim Racing is not a state-licensed driver-education provider, and '
            'simulator hours do not satisfy Florida licensing requirements.',
            'Simulator training supplements real-world driving instruction. It does not '
            'replace required behind-the-wheel experience.',
        ],
    ),
    'health': dict(
        name='Academy Sim Racing, Simulator Programs for Seniors and 55+ Communities',
        facts=[
            'Low-impact racing simulator programs run on site at senior living communities, '
            '55+ communities and rehabilitation settings, in Tampa and statewide Florida.',
            'Academy Sim Racing provides simulator experiences and structured programs. '
            'We are not a medical provider.',
            'Nothing on this site is a medical claim, a treatment or a clinical outcome.',
        ],
    ),
}

SHARED = ('Academy Sim Racing is a veteran-owned business based in Tampa, Florida. '
          'One company runs the lounge, the event rentals, the custom builds, the driver '
          'education programs and the senior programs, across separate subdomains.')

# Per-page notes, 2026-09-09. A one-line llms.txt entry cannot carry the disclaimers
# the page itself makes, and llms.txt is read by machines that will not fetch the page.
# Each entry is emitted as an indented sub-bullet directly under its page line. The
# self-check below FAILS the build if a builds /tracks/ page has no note, so a new
# circuit page cannot ship a bare line by accident.
NOTES = {
    ('builds', '/tracks/sebring-racing-simulator/'):
        'Not affiliated with, endorsed by or partnered with Sebring International Raceway. '
        'The build is at Sebring Motor Garages, an independent clubhouse and garage-condo '
        'community near the circuit; Academy operates no branch at the track.',
}

# Nicer names for the first path segment. Anything unlisted is title-cased.
SECTIONS = {
    'racing': 'Racing disciplines',
    'tracks': 'Tracks',
    'cars': 'Cars',
    'cars-and-tracks': 'Cars and tracks',
    'event-types': 'Event types',
    'locations': 'Locations served',
    'experiences': 'Experiences',
    'for': 'Who the builds are for',
    'simulators': 'Simulators',
    'network': 'Network',
    'school-districts': 'Florida school districts',
    'programs': 'Programs',
    'things-to-do-in-tampa': 'Tampa',
}


def clean(s):
    """Unescape, collapse whitespace, apply the house em dash rule."""
    s = html.unescape(s or '')
    s = EMDASH.sub(', ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.replace(' ,', ',').replace(',,', ',')
    return s


BRAND = ('academy', 'academy sim racing', "academy driver's ed", 'academy drivers ed',
         'academy sim racing tampa', 'academy builds', 'academy events')


def strip_brand(title):
    """Drop the repeated brand furniture so the list reads as a list.

    Titles carry the brand in a trailing (or leading) pipe segment, and repeating
    it on all 27 lines tells a reader nothing. Split on the separator, drop the
    segments that are only the brand, and rejoin with a SPACED pipe: rejoining on
    the bare separator is what produced 'Programs Across Florida|Academy'.
    Never return empty - a title that is nothing but brand keeps the brand.
    """
    t = clean(title)
    for sep in ('|', '–'):
        if sep not in t:
            continue
        parts = [p.strip() for p in t.split(sep) if p.strip()]
        kept = [p for p in parts if p.lower().strip(' .,') not in BRAND]
        t = ' | '.join(kept) if kept else (parts[0] if parts else t)
    return re.sub(r'\s+', ' ', t).strip(' ,|-')


def meta(path):
    s = io.open(path, encoding='utf-8', errors='replace', newline='').read()
    t = re.search(r'<title[^>]*>(.*?)</title>', s, re.S | re.I)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
                  s, re.S | re.I)
    return strip_brand(t.group(1) if t else ''), clean(d.group(1) if d else '')


def local_for(key, url_path):
    """Map a live URL path back to the staged file. upload/ wins: it holds the fixes."""
    rel = url_path.strip('/')
    rel = 'index.html' if not rel else (rel if rel.endswith('.html') else rel + '/index.html')
    for base in ('upload', 'site', 'source'):
        p = os.path.join(ROOT, key, base, rel.replace('/', os.sep))
        if os.path.exists(p):
            return p
    return None


def build(key):
    cfg = SITES[key]
    sm = os.path.join(ROOT, key, 'site', 'sitemap.xml')
    if not os.path.exists(sm):
        return None, ['no sitemap.xml']
    xml = io.open(sm, encoding='utf-8').read()
    locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', xml)

    problems, rows = [], []
    for loc in locs:
        path = re.sub(r'^https?://[^/]+', '', loc) or '/'
        f = local_for(key, path)
        if not f:
            problems.append('no local file for %s' % path)
            continue
        title, desc = meta(f)
        if not title:
            problems.append('no <title> for %s' % path)
        rows.append((path, loc, title, desc))

    # Homepage first, then sections in sitemap order, pages sorted inside each.
    order, groups = [], {}
    home = None
    for path, loc, title, desc in rows:
        if path == '/':
            home = (loc, title, desc)
            continue
        seg = path.strip('/').split('/')[0].replace('.html', '')
        name = SECTIONS.get(seg, seg.replace('-', ' ').capitalize())
        if name not in groups:
            groups[name] = []
            order.append(name)
        groups[name].append((path, loc, title, desc))

    out = []
    out.append('# %s' % cfg['name'])
    out.append('')
    if home and home[2]:
        out.append('> %s' % (home[2] if home[2] else home[1]))
        out.append('')
    out.append(SHARED)
    out.append('')
    out.append('## What an assistant should get right about this site')
    out.append('')
    for f in cfg['facts']:
        out.append('- %s' % f)
    out.append('')
    if home:
        out.append('## Start here')
        out.append('')
        out.append('- [%s](%s)%s' % (home[1], home[0], ': ' + home[2] if home[2] else ''))
        out.append('')
    for name in order:
        out.append('## %s' % name)
        out.append('')
        for path, loc, title, desc in sorted(groups[name], key=lambda r: r[0]):
            out.append('- [%s](%s)%s' % (title or path, loc, ': ' + desc if desc else ''))
            note = NOTES.get((key, path))
            if note:
                out.append('  - Note: %s' % note)
        out.append('')
    out.append('## Optional')
    out.append('')
    out.append('- [Sitemap](%s/sitemap.xml): every live URL on this subdomain.' % HOSTS[key])
    out.append('')

    text = '\n'.join(out)

    # Self-checks. These are the audit rules that apply to authored copy, and
    # llms.txt is authored copy.
    if re.search(r'&mdash;|—', text):
        problems.append('EM-DASH survived the transform')
    for loc in locs:
        if loc not in text:
            problems.append('sitemap URL missing from output: %s' % loc)
    if key == 'builds':
        for path, loc, title, desc in rows:
            if path.startswith('/tracks/') and (key, path) not in NOTES:
                problems.append('builds circuit page has no disclaimer NOTE: %s' % path)
    for (k, path), note in NOTES.items():
        if k == key and ('  - Note: %s' % note) not in text:
            problems.append('NOTE not emitted for %s' % path)
    if len(text.encode('utf-8')) > 100000:
        problems.append('over 100 KB')
    return text, problems


def main(keys):
    bad = 0
    for key in keys:
        text, problems = build(key)
        if text is None:
            print('%-7s !! %s' % (key, '; '.join(problems)))
            bad += 1
            continue
        written = []
        for base in ('site', 'upload'):
            d = os.path.join(ROOT, key, base)
            if not os.path.isdir(d):
                continue
            p = os.path.join(d, 'llms.txt')
            io.open(p, 'w', encoding='utf-8', newline='\n').write(text)
            written.append(base)
        n = text.count('\n- [')
        print('%-7s %2d links, %5d bytes -> %s' % (key, n, len(text.encode('utf-8')),
                                                   ', '.join(w + '/llms.txt' for w in written)))
        for p in problems:
            print('        !! %s' % p)
            bad += 1
    if bad:
        raise SystemExit('  %d problem(s)' % bad)
    print('\n  llms.txt clean')


if __name__ == '__main__':
    main(sys.argv[1:] or ['lounge', 'events', 'builds', 'driver', 'health'])

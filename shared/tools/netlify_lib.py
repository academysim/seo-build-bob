# -*- coding: utf-8 -*-
"""Shared Netlify helpers: token, curl wrapper, and live-deploy manifest fetch."""
import io, json, os, subprocess

API = 'https://api.netlify.com/api/v1'

SITES = {
    'lounge': '01b3c52d-9270-4cfe-a813-bc56a1f7f613',
    'events': '572f7d55-3233-45c1-9326-ed4cc83de191',
    'builds': '1bd1c472-c35a-499e-a801-28129b07dcea',
    'driver': '54be937f-a303-465e-a88c-951a4674087a',
    'health': '96bc6485-c4bc-49d7-a994-9db282d0be50',
}


def token():
    for line in io.open('HACKATHON-FORK-NO-DEPLOY/.env.local', encoding='utf-8', errors='replace'):
        if line.split('=')[0].strip().upper() in ('NETLIFY_AUTH_TOKEN', 'NETLIFY_TOKEN'):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('no netlify token in HACKATHON-FORK-NO-DEPLOY/.env.local')


def curl(args, data=None, binary=None, tok=None):
    tok = tok or token()
    cmd = ['curl.exe', '-s', '-H', 'Authorization: Bearer ' + tok] + args
    if data is not None:
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
        return subprocess.run(cmd, input=data.encode('utf-8'),
                              stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')
    if binary is not None:
        cmd += ['-H', 'Content-Type: application/octet-stream', '--data-binary', '@' + binary]
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')


def live_manifest(key):
    """The published deploy's complete file list: [{path, sha}, ...]."""
    tok = token()
    site = json.loads(curl(['%s/sites/%s' % (API, SITES[key])], tok=tok))
    dep_id = site['published_deploy']['id']
    files = json.loads(curl(['%s/deploys/%s/files' % (API, dep_id)], tok=tok))
    return dep_id, [{'path': f['path'], 'sha': f['sha']} for f in files]


if __name__ == '__main__':
    import sys
    for key in (sys.argv[1:] or list(SITES)):
        dep, fs = live_manifest(key)
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '..', '..', key, 'tools', '%s_files.json' % key)
        out = os.path.normpath(out)
        io.open(out, 'w', encoding='utf-8').write(json.dumps(fs, indent=1))
        print('%-8s deploy %s  %3d files -> %s' % (key, dep, len(fs), out))

# -*- coding: utf-8 -*-
"""Copy the SEO build tooling and sources out of the session scratchpad, which
is temporary, into a durable repo on D:.

Organised per property so someone opening it cold can tell what runs what.
Nothing here contains credentials: the deploy scripts read NETLIFY_AUTH_TOKEN
from D:\\AcademyPipeline\\.env.local at runtime.
"""
import io, os, shutil

SRC = os.path.dirname(os.path.abspath(__file__))
DST = 'D:/AcademySimRacing/03-SEO-Build'

# tool -> subfolder
LAYOUT = {
    'lounge': ['assemble.py', 'audit_site.py', 'finalise_pages.py', 'strip_dashes.py',
               'fix_batch2.py', 'fix_batch3.py', 'fix_cars_r1.py', 'fix_daytona_corners.py',
               'fix_daytona_r2.py', 'fix_tampa_r1.py', 'fix_clutch.py', 'fix_round4.py',
               'fix_nav_eyebrow.py', 'fix_prose_links.py', 'fix_scroll.py', 'fix_img_size.py',
               'fix_audit.py', 'fix_tracking_gaps.py', 'add_images.py', 'add_tracking.py',
               'stage_tracks.py', 'stage_cars.py', 'stage_library.py', 'stage_manual.py',
               'verify_all.py', 'probe_live.py'],
    'events': ['events_pages.py', 'events_content.py', 'events_content2.py', 'events_content3.py',
               'events_content4.py', 'events_content5.py', 'events_audit.py', 'events_deploy.py',
               'events_extract.py', 'events_mirror.py', 'fix_events_r1.py', 'fix_events_r2.py',
               'fix_events_specs.py', 'fix_events_claims.py', 'fix_hub_links.py'],
    'builds': ['builds_pages.py', 'builds_content.py', 'builds_content2.py', 'builds_content3.py',
               'builds_audit.py', 'builds_deploy.py', 'fix_network_block.py'],
    'driver': ['driver_pages.py', 'driver_content.py', 'driver_content2.py', 'driver_content3.py',
               'driver_audit.py', 'driver_deploy.py', 'fix_driver_licensing.py'],
    'health': ['health_pages.py', 'health_content.py', 'health_content2.py',
               'health_audit.py', 'health_deploy.py'],
    'shared': ['fix_americanize.py', 'edit_homepages.py', 'rebuild_index.py',
               'solve_form_order.py', 'derive_transform.py', 'recover_sources.py',
               'update_docs.py', 'update_docs2.py', 'update_docs3.py', 'record_solve.py',
               'preserve.py'],
}

# generated site trees worth keeping (the deployable output)
TREES = {
    'lounge': 'lounge_deploy',
    'events': 'events_new',
    'builds': 'builds_new',
    'driver': 'driver_new',
    'health': 'health_new',
}

# the extracted templates each generator depends on
PARTS = {
    'lounge': 'lounge_build',
    'events': 'events_build',
    'builds': 'builds_build',
    'driver': 'driver_build',
    'health': 'health_build',
}

copied = 0
for folder, names in LAYOUT.items():
    d = os.path.join(DST, folder, 'tools')
    os.makedirs(d, exist_ok=True)
    for n in names:
        p = os.path.join(SRC, n)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(d, n))
            copied += 1

trees = 0
for folder, tree in TREES.items():
    s = os.path.join(SRC, tree)
    if os.path.isdir(s):
        d = os.path.join(DST, folder, 'site')
        if os.path.isdir(d):
            shutil.rmtree(d)
        shutil.copytree(s, d)
        trees += 1

for folder, part in PARTS.items():
    s = os.path.join(SRC, part)
    if os.path.isdir(s):
        d = os.path.join(DST, folder, 'template')
        if os.path.isdir(d):
            shutil.rmtree(d)
        shutil.copytree(s, d, ignore=shutil.ignore_patterns('*.md'))

# the briefs that governed everything
b = os.path.join(SRC, 'seozip')
if os.path.isdir(b):
    d = os.path.join(DST, 'brief')
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(b, d)

print('  %d tool files, %d site trees copied to %s' % (copied, trees, DST))
for root, dirs, files in os.walk(DST):
    if root.count(os.sep) - DST.count(os.sep) <= 1:
        rel = os.path.relpath(root, DST)
        print('    %-22s %d files' % (rel, len(files)))

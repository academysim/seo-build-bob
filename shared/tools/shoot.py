# -*- coding: utf-8 -*-
"""Full-page screenshots, desktop and real mobile emulation, via Playwright Chromium.

  python shoot.py <outdir> <url> [url ...]            desktop 1366 + iPhone-class mobile (390x844 @2x, touch)
  python shoot.py <outdir> --desktop-only <url ...>
  python shoot.py <outdir> --mobile-only  <url ...>
  python shoot.py <outdir> --sheet                      rebuild contact sheets from PNGs already in <outdir>

Writes <outdir>/<slug>.desktop.png and <slug>.mobile.png (full page, capped at 9000 px tall), then
contact sheets sheet-desktop-N.jpg / sheet-mobile-N.jpg with 4 pages per sheet so a reviewer can Read them.
Why Playwright: headless Chrome's --window-size refuses widths under about 500 px on this box, so
true phone layouts (390 px) can only be produced with device emulation.
"""
import os, re, sys, glob
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

MOBILE = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
              user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
DESKTOP = dict(viewport={'width': 1366, 'height': 900}, device_scale_factor=1)


def slug(u):
    s = re.sub(r'^https?://', '', u).strip('/').replace('/', '__')
    return re.sub(r'[^A-Za-z0-9._-]+', '-', s) or 'root'


def shoot(out, urls, modes):
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for mode, opts in modes:
            ctx = browser.new_context(**opts)
            page = ctx.new_page()
            for u in urls:
                path = os.path.join(out, '%s.%s.png' % (slug(u), mode))
                try:
                    page.goto(u, wait_until='networkidle', timeout=60000)
                    page.wait_for_timeout(1200)
                    h = page.evaluate('document.documentElement.scrollHeight')
                    w = page.evaluate('document.documentElement.scrollWidth')
                    vw = opts['viewport']['width']
                    page.screenshot(path=path, full_page=True, clip={'x': 0, 'y': 0, 'width': vw, 'height': min(h, 9000)})
                    print('  %-8s %-70s %5d px tall%s' % (mode, u[:70], h, '  HORIZONTAL OVERFLOW %dpx' % w if w > vw + 2 else ''))
                except Exception as e:
                    print('  %-8s %-70s FAILED %s' % (mode, u[:70], str(e)[:80]))
            ctx.close()
        browser.close()


def sheets(out):
    for mode, per_w, sheet_h in (('desktop', 660, 1400), ('mobile', 300, 1500)):
        files = sorted(glob.glob(os.path.join(out, '*.%s.png' % mode)))
        for n in range(0, len(files), 4):
            group = files[n:n + 4]
            sheet = Image.new('RGB', (per_w * 4, sheet_h), 'black')
            d = ImageDraw.Draw(sheet)
            for i, f in enumerate(group):
                im = Image.open(f).convert('RGB')
                im.thumbnail((per_w - 8, sheet_h - 26))
                sheet.paste(im, (i * per_w + 4, 4))
                d.text((i * per_w + 6, sheet_h - 18), os.path.basename(f)[:60], fill='white')
            sp = os.path.join(out, 'sheet-%s-%d.jpg' % (mode, n // 4 + 1))
            sheet.save(sp, quality=82)
            print('  sheet', sp)


if __name__ == '__main__':
    out = sys.argv[1]
    args = sys.argv[2:]
    if args and args[0] == '--sheet':
        sheets(out); sys.exit()
    modes = [('desktop', DESKTOP), ('mobile', MOBILE)]
    if args and args[0] == '--desktop-only': modes = modes[:1]; args = args[1:]
    if args and args[0] == '--mobile-only': modes = modes[1:]; args = args[1:]
    shoot(out, args, modes)
    sheets(out)

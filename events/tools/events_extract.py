# -*- coding: utf-8 -*-
"""Pull the reusable template out of the live events homepage."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'events_deploy', 'index.html')
OUT = os.path.join(HERE, 'events_build')
if not os.path.isdir(OUT):
    os.makedirs(OUT)

s = io.open(SRC, encoding='utf-8', errors='replace', newline='').read()


def w(name, text):
    p = os.path.join(OUT, name)
    io.open(p, 'w', encoding='utf-8', newline='').write(text)
    print('  %-22s %d bytes' % (name, len(text.encode())))


# style
m = re.search(r'<style[^>]*>(.*?)</style>', s, re.S)
w('_style.css', m.group(1).strip())

# nav
m = re.search(r'<nav class="nav">.*?</nav>', s, re.S)
w('_nav.html', m.group(0).strip())

# footer
m = re.search(r'<footer class="footer">.*?</footer>', s, re.S)
w('_footer.html', m.group(0).strip())

# head links: fonts, icons, analytics
head = s.split('</head>')[0]
keep = []
for pat in (r'<link rel="preconnect"[^>]*>', r'<link[^>]*fonts\.googleapis[^>]*>',
            r'<link rel="icon"[^>]*>', r'<link rel="apple-touch-icon"[^>]*>',
            r'<link rel="manifest"[^>]*>'):
    keep += re.findall(pat, head)
w('_headlinks.html', '\n'.join(keep))

# analytics block
m = re.search(r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>\s*<script>.*?</script>', head, re.S)
w('_ga.html', m.group(0).strip() if m else '')

# the quote form, verbatim, so a copy on a landing page keeps working
for name in ('event-quote', 'event-schedule'):
    m = re.search(r"<form[^>]*name='%s'[^>]*>.*?</form>" % name, s, re.S)
    if m:
        w('_form-%s.html' % name, m.group(0).strip())

# what classes exist, so new pages only use real ones
classes = sorted(set(re.findall(r'\.([a-z][a-z0-9-]+)\s*\{', m.group(0) if False else
                                re.search(r'<style[^>]*>(.*?)</style>', s, re.S).group(1))))
w('_classes.txt', '\n'.join(classes))
print('\n  %d css classes available' % len(classes))

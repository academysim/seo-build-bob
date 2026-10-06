"""Remove em dashes from customer-facing copy without touching code.

Safe zones only: everything EXCEPT <style> blocks and non-JSON-LD <script>
blocks. JSON-LD is included deliberately, because those strings are shown in
search results, but the result is re-parsed to prove it still validates.
"""
import io, re, sys, json



CHROME = (r'<nav\b[^>]*>.*?</nav>|'
          r'<footer\b[^>]*>.*?</footer>|')

def split_protected(s, keep_chrome=False):
    """Yield (text, is_protected) spans."""
    pat = re.compile(r'(' + (CHROME if keep_chrome else '') +
                     r'<style\b[^>]*>.*?</style>|<script\b(?![^>]*application/ld\+json)[^>]*>.*?</script>)', re.S | re.I)
    pos = 0
    for m in pat.finditer(s):
        if m.start() > pos:
            yield s[pos:m.start()], False
        yield m.group(0), True
        pos = m.end()
    if pos < len(s):
        yield s[pos:], False


def fix(text):
    # " — " between clauses becomes a comma; a dash hugging words becomes a comma too.
    text = re.sub(r'\s*&mdash;\s*', ', ', text)
    text = re.sub(r'\s*—\s*', ', ', text)
    # JSON-LD writes the dash as the escape \u2014, which the literal
    # patterns above cannot match. Missing it let structured data keep a dash
    # while the visible text lost one, so the two disagreed.
    text = re.sub(r'\s*\\u2014\s*', ', ', text)
    # tidy artefacts
    text = text.replace(', ,', ',').replace(' ,', ',').replace(',,', ',')
    text = re.sub(r',\s*\.', '.', text)
    text = re.sub(r'\.\s*,', '.', text)
    return text


def process(path_in, path_out, keep_chrome=False):
    s = io.open(path_in, encoding='utf-8', newline='').read()
    before = len(re.findall(r'&mdash;|—|\\u2014', s))
    out = []
    changed_protected = 0
    for span, protected in split_protected(s, keep_chrome):
        if protected:
            changed_protected += len(re.findall(r'&mdash;|—|\\u2014', span))
            out.append(span)
        else:
            out.append(fix(span))
    r = ''.join(out)
    after = len(re.findall(r'&mdash;|—|\\u2014', r))

    # every JSON-LD block must still parse
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', r, re.S)
    for b in blocks:
        json.loads(b)

    # Structural sanity: nothing but dash/comma punctuation and the whitespace
    # around it may differ. The first version of this check compared without
    # normalising whitespace and fired on every file, because turning " — "
    # into ", " changes the space count. That was the check being wrong, not
    # the edit.
    def skeleton(x):
        x = re.sub(r'&mdash;|—|\\u2014', '', x)
        x = re.sub(r'[,\s]+', '', x)
        return x
    a, bb = skeleton(s), skeleton(r)
    if a != bb:
        for i in range(min(len(a), len(bb))):
            if a[i] != bb[i]:
                raise AssertionError("real change at offset %d: %r vs %r" % (i, a[i-60:i+60], bb[i-60:i+60]))
        raise AssertionError("length differs: %d vs %d" % (len(a), len(bb)))

    io.open(path_out, 'w', encoding='utf-8', newline='').write(r)
    print("  %-28s dashes %d -> %d (left in code: %d) | json-ld blocks ok: %d | %d -> %d bytes"
          % (path_in.split('\\')[-1], before, after, changed_protected, len(blocks),
             len(s.encode()), len(r.encode())))
    return r


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--keep-chrome']
    process(args[0], args[1], keep_chrome='--keep-chrome' in sys.argv)

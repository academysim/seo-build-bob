import sys, io, os
sys.path.insert(0, 'shared/tools')
import audit_discovery as A

ADDR = '"address":{"@type":"PostalAddress","streetAddress":"1421 Massaro Blvd","addressLocality":"Tampa"}'

def ld(body):
    return '<html><script type="application/ld+json">%s</script></html>' % body

CASES = [
    # (name, html, expected premises_claim, why)
    ('top-level LocalBusiness with address (the real risk)',
     ld('{"@type":"LocalBusiness","name":"X",%s}' % ADDR), True,
     'a page claiming a business AT this location'),
    ('LocalBusiness nested as a Service provider (correct markup)',
     ld('{"@type":"Service","provider":{"@type":"LocalBusiness","name":"X",%s}}' % ADDR), False,
     'declaring the real provider is not a premises claim'),
    ('the words in an HTML comment only',
     '<html><!-- Service / LocalBusiness structured data --><p>PostalAddress</p></html>', False,
     'the old substring test fired on exactly this'),
    ('LocalBusiness with NO address',
     ld('{"@type":"LocalBusiness","name":"X"}'), False,
     'no address means no location claim'),
    ('@graph containing a top-level LocalBusiness',
     ld('{"@graph":[{"@type":"WebSite"},{"@type":"LocalBusiness",%s}]}' % ADDR), True,
     'must see through @graph'),
    ('@type as a list including LocalBusiness',
     ld('{"@type":["Organization","LocalBusiness"],%s}' % ADDR), True,
     'must handle list-valued @type'),
    ('unparseable JSON-LD',
     ld('{"@type":"LocalBusiness", oops}'), False,
     'a broken block is caught by the JSON-LD check, not this one'),
]

fails = 0
for name, html, expected, why in CASES:
    got = A.premises_claim(html)
    ok = (got == expected)
    print('%-4s %-58s expected=%-5s got=%-5s  (%s)' %
          ('OK' if ok else 'FAIL', name, expected, got, why))
    if not ok:
        fails += 1

# The URL allowlist half
URLS = [
    ('https://builds.academysim.com/', True, 'homepage represents the company'),
    ('https://events.academysim.com/', True, 'homepage'),
    ('https://lounge.academysim.com/things-to-do-in-tampa/', True, 'explicitly allowed'),
    ('https://events.academysim.com/locations/orlando/', False, 'CITY PAGE must stay guarded'),
    ('https://health.academysim.com/locations/sarasota/', False, 'CITY PAGE must stay guarded'),
    ('https://builds.academysim.com/network/', False, 'sub-page must stay guarded'),
]
print()
for u, expected, why in URLS:
    got = bool(A.PREMISES_OK.match(u.rstrip('/') + '/'))
    ok = (got == expected)
    print('%-4s %-52s allowed=%-5s expected=%-5s  (%s)' %
          ('OK' if ok else 'FAIL', u, got, expected, why))
    if not ok:
        fails += 1

print()
if fails:
    raise SystemExit('%d GATE TEST FAILURE(S)' % fails)
print('all gate tests pass: the relaxed rule still catches a real premises claim')

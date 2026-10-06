# -*- coding: utf-8 -*-
"""Edit the events and builds homepages, now that both are byte-identically
reconstructable and therefore safe to redeploy.

Events:
  1. correct the throughput figure from 15-30 to 15-40 (Malik's number), in the
     visible FAQ answer AND in the FAQ JSON-LD, which is the half that would
     otherwise keep feeding the wrong number to Google
  2. link the three new sections, which were previously reachable only from the
     sitemap

Builds:
  1. link /simulators/, /for/ and /network/
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- EVENTS --
p = os.path.join(HERE, 'events_new', 'index.html')
s = io.open(p, encoding='utf-8', newline='').read()
before = len(s.encode())

old_n = 'Depending on session length, expect 15–30 racers per hour per simulator.'
new_n = 'Depending on session length, expect 15–40 racers per hour per simulator.'
n_fix = s.count(old_n)
s = s.replace(old_n, new_n)

NAV_SECTION = '''<section class="section">
  <div class="section-head">
    <div class="eyebrow">Plan Your Event</div>
    <h2 class="h2">EVERYTHING, IN DETAIL</h2>
    <p class="section-intro">Guidance on the format, the racing and the logistics, written for planners rather than for search engines.</p>
  </div>
  <div class="types-grid">
    <a class="type-card" href="/event-types/" style="text-decoration:none;">
      <div class="type-num">01 / By Event Type</div>
      <div class="type-name">CORPORATE, TRADE SHOWS, MORE</div>
      <div class="type-desc">Ten event formats covered properly: corporate events, trade shows, conventions, brand activations, dealership events, watch parties, employee appreciation, client entertainment, private parties and fundraisers.</div>
    </a>
    <a class="type-card" href="/experiences/" style="text-decoration:none;">
      <div class="type-num">02 / By Racing Type</div>
      <div class="type-name">PICK THE RIGHT FORMAT</div>
      <div class="type-desc">GT3, Formula-style, stock car, endurance, drift and rally. Which one suits your room, and why putting a corporate audience in the fastest car is usually the wrong call.</div>
    </a>
    <a class="type-card" href="/locations/" style="text-decoration:none;">
      <div class="type-num">03 / Where We Deliver</div>
      <div class="type-name">ACROSS FLORIDA</div>
      <div class="type-desc">Tampa, Orlando, Daytona Beach and Sarasota in detail, plus how mobile delivery works from our Tampa base to anywhere else in the state.</div>
    </a>
  </div>
</section>

'''

anchor = '<section class="faq">'
assert s.count(anchor) == 1, 'events faq anchor x%d' % s.count(anchor)
if 'Plan Your Event' not in s:
    s = s.replace(anchor, NAV_SECTION + anchor, 1)
    added = True
else:
    added = False

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('EVENTS')
print('  15-30 -> 15-40 replacements : %d  (visible copy + FAQ JSON-LD)' % n_fix)
print('  new-section nav added       : %s' % added)
print('  %d -> %d bytes' % (before, len(s.encode())))

# ---------------------------------------------------------------- BUILDS --
p = os.path.join(HERE, 'builds_new', 'index.html')
s = io.open(p, encoding='utf-8', newline='').read()
before = len(s.encode())

BUILDS_SECTION = '''<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Work Out What You Need</span>
      <h2>Before you <span class="accent">choose a tier.</span></h2>
      <p>The lineup above is the what. These are the how and the why, written to help you spec it rather than to sell you up a tier.</p>
    </div>
    <div class="linkgrid">
      <a class="linkcard" href="/simulators/">
        <div class="lc-name">SPEC IT BY DISCIPLINE</div>
        <div class="lc-desc">GT3, formula, stock car, endurance, drift, rally, track day, triple screen and motion. What each one actually needs from a rig, and where we would put the budget.</div>
      </a>
      <a class="linkcard" href="/for/">
        <div class="lc-name">BY WHO IT IS FOR</div>
        <div class="lc-desc">Track drivers, race teams, collectors, luxury garages, garage condos, dealerships, offices, hotels and clubs. The brief changes the spec more than the budget does.</div>
      </a>
      <a class="linkcard" href="/network/">
        <div class="lc-name">SEE ONE IN PERSON</div>
        <div class="lc-desc">Where you can actually drive one before you commit, and the three decisions that are genuinely worth travelling for.</div>
      </a>
    </div>
  </div>
</section>

'''

anchor = '<section class="faq" id="faq">'
assert s.count(anchor) == 1, 'builds faq anchor x%d' % s.count(anchor)
if 'Work Out What You Need' not in s:
    s = s.replace(anchor, BUILDS_SECTION + anchor, 1)
    added = True
else:
    added = False

# the new pages define .linkgrid/.linkcard in their own <style>; the homepage
# does not, so the rules have to come with the section
CSS = ('\n.linkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem;margin-top:1.5rem;}'
       '\n.linkcard{display:block;border:1px solid var(--border);border-radius:12px;padding:1.15rem;'
       'text-decoration:none;transition:transform .15s,border-color .15s;}'
       '\n.linkcard:hover{transform:translateY(-2px);border-color:var(--gold);}'
       "\n.lc-name{font-family:'Bebas Neue',sans-serif;font-size:1.15rem;letter-spacing:0.02em;margin-bottom:.3rem;}"
       '\n.lc-desc{font-size:0.86rem;color:var(--muted);line-height:1.5;}\n')
if '.linkcard{' not in s:
    i = s.rindex('</style>')
    s = s[:i] + CSS + s[i:]
    css_added = True
else:
    css_added = False

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('\nBUILDS')
print('  new-section nav added : %s' % added)
print('  linkgrid css added    : %s' % css_added)
print('  %d -> %d bytes' % (before, len(s.encode())))

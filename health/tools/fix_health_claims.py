# -*- coding: utf-8 -*-
"""P0: bring the health.academysim.com homepage inside its own claims rules.

The post-implementation audit called Health "the highest content-risk area" and
asked for two things: replace absolute safety language, and stop presenting
research findings as guaranteed Academy outcomes. Checking the sources turned up
a third, worse problem.

**The Cochrane citation contradicted the page.** The homepage carried a stat card
reading "~33% of stroke survivors need structured driving rehabilitation before
safely returning to the road", attributed to George et al., Cochrane Review
(2014). That review contains no such figure. Its actual conclusion, across four
trials and 245 participants, is that there was INSUFFICIENT EVIDENCE to reach
conclusions about rehabilitation improving on-road driving skill after stroke.
The page was citing, as proof that the thing works, a review that concluded the
evidence is not there. That card is now replaced with what the review really
found.

**The Akinwuntan percentages could not be confirmed.** "73% ... vs. 42%" is
consistent with the study's reported effect but no accessible source states those
exact figures. Per the audit rule on unverified numbers, it is now the sourced
qualitative finding ("close to twice as likely") with the citation kept.

Everything else follows one principle, taken from the sibling pages that already
pass health_audit.py: **describe what a session involves, never what it will do
to somebody.** Outcome verbs applied to health nouns (improves attention,
sharpens executive function, reduces depression, supports MCI intervention) are
replaced with plain descriptions of the activity. A disclaimer at the bottom does
not cure a promise in the body.

Reads  health/source/index.html  (byte-exact, SHA-verified against the live store)
Writes health/upload/index.html
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source', 'index.html')
DST = os.path.join(HERE, '..', 'upload')

EM = u'—'

# ---------------------------------------------------------------- edits ----
# (old, new, expected_count). Order matters only where one edit's output would
# otherwise be matched by a later edit.
EDITS = [

    # ============ A. absolute safety language =============================
    # "Zero Fall Risk" promises an outcome no operator can guarantee for a
    # person transferring into a fixed racing seat. The defensible claim is
    # what is actually true of the setup: seated, supervised, off the road.
    (u'Wheelchair Accessible \xb7 Fully Staffed \xb7 Zero Fall Risk',
     u'Wheelchair Accessible \xb7 Fully Staffed \xb7 Seated and Supervised', 1),

    (u'<div class="trust-item"><div class="trust-label">Risk</div>'
     u'<div class="trust-val">Zero Falls</div></div>',
     u'<div class="trust-item"><div class="trust-label">Setting</div>'
     u'<div class="trust-val">Seated</div></div>', 1),

    (u'<li>Zero fall risk, zero road risk</li>',
     u'<li>Seated throughout, with no on-road exposure</li>', 1),

    (u'<span class="chk">✓</span> Zero risk of falls or road injury',
     u'<span class="chk">✓</span> Seated, supervised, no on-road exposure', 1),

    (u'gentle, repeatable motor practice without physical risk.',
     u'gentle, repeatable movement with no on-road exposure.', 1),

    (u'in a zero-risk environment as part of a structured rehab plan.',
     u'in a controlled environment, as part of a plan run by that person’s '
     u'own clinical team.', 1),

    # FAQ answer, in the visible copy AND the FAQPage JSON-LD. Structured data
    # left behind keeps asserting a claim the page no longer makes.
    (u'Yes. Because everything happens in a simulator, there’s no risk of '
     u'collision, falls, or physical harm.',
     u'Everything happens in a simulator, so there is no on-road collision '
     u'exposure, and participants stay seated and supervised throughout.', 0),
    (u"Yes. Because everything happens in a simulator, there's no risk of "
     u"collision, falls, or physical harm.",
     u'Everything happens in a simulator, so there is no on-road collision '
     u'exposure, and participants stay seated and supervised throughout.', 2),

    # ============ B. outcome claims on health nouns ========================
    (u'this is how seniors stay sharp, engaged, and smiling.',
     u'it gives older adults something genuinely worth looking forward to.', 1),

    # The benefits section promised results. It now describes the activity.
    (u'<div class="eyebrow">The Benefits</div>',
     u'<div class="eyebrow">What A Session Involves</div>', 1),
    (u'<h2 class="h2">THREE KINDS OF GOOD ' + EM + u' ALL AT ONCE</h2>',
     u'<h2 class="h2">THREE THINGS IT ASKS AT ONCE</h2>', 1),
    (u'<a class="btn-ghost" href="#benefits">SEE THE BENEFITS</a>',
     u'<a class="btn-ghost" href="#benefits">WHAT A SESSION INVOLVES</a>', 1),
    (u'Research consistently shows driving-simulator activity benefits older '
     u'adults across cognitive, physical, and social dimensions. Unlike a '
     u'crossword or a walk, it exercises all three at the same time.',
     u'Driving asks for attention, judgement and coordination at the same time, '
     u'which is what makes it absorbing. Here is what a session actually '
     u'involves. Published research on simulator training in older adults is '
     u'summarized further down this page.', 1),

    (u'<div class="why-name">COGNITIVE BENEFITS</div>',
     u'<div class="why-name">COGNITIVE DEMANDS</div>', 1),
    (u'<div class="why-name">PHYSICAL BENEFITS</div>',
     u'<div class="why-name">PHYSICAL DEMANDS</div>', 1),

    # noun phrases describe the task; verbs like "improves" and "sharpens"
    # promise a clinical result, and "Supports MCI intervention" is a medical
    # claim outright.
    (u'        <li>Improves divided visual attention</li>\n'
     u'        <li>Sharpens executive function</li>\n'
     u'        <li>Exercises working memory</li>\n'
     u'        <li>Strengthens reaction time</li>\n'
     u'        <li>Supports MCI intervention</li>\n',
     u'        <li>Divided visual attention</li>\n'
     u'        <li>Planning and decision-making</li>\n'
     u'        <li>Working memory for routes and signs</li>\n'
     u'        <li>Reacting to changing conditions</li>\n', 1),

    (u'        <li>Maintains fine motor control</li>\n'
     u'        <li>Practices hand-eye coordination</li>\n'
     u'        <li>Improves pedal &amp; braking response</li>\n'
     u'        <li>Encourages postural engagement</li>\n',
     u'        <li>Fine motor control</li>\n'
     u'        <li>Hand-eye coordination</li>\n'
     u'        <li>Pedal and braking movement</li>\n'
     u'        <li>Seated postural engagement</li>\n', 1),

    # "Combats social isolation" and "Reduces driving-loss depression" are
    # treatment claims. Depression is a diagnosis; Academy does not treat it.
    (u'        <li>Combats social isolation</li>\n'
     u'        <li>Builds confidence &amp; self-efficacy</li>\n'
     u'        <li>Provides joyful, purposeful activity</li>\n'
     u'        <li>Reduces driving-loss depression</li>\n'
     u'        <li>Creates shared family experiences</li>\n',
     u'        <li>Brings residents together</li>\n'
     u'        <li>A chance to feel capable again</li>\n'
     u'        <li>Something to look forward to</li>\n'
     u'        <li>Something to talk about afterwards</li>\n'
     u'        <li>Shared family experiences</li>\n', 1),

    (u'Simulators make that path safer, measurable, and more likely to succeed.',
     u'Simulator sessions can form part of a program run by that person’s '
     u'own clinical team.', 1),

    # Academy does not deliver cognitive rehabilitation to patients.
    (u'      <div class="stroke-name">Cognitive Rehabilitation</div>\n'
     u'      <div class="stroke-desc">Targeted attention, executive function, '
     u'and spatial awareness work for patients with MCI, TBI, or early '
     u'dementia.</div>',
     u'      <div class="stroke-name">Alongside Clinical Programs</div>\n'
     u'      <div class="stroke-desc">Simulator time can be scheduled around an '
     u'occupational therapy or driving rehabilitation program that a qualified '
     u'professional is running. Academy does not assess, diagnose or treat.</div>',
     1),

    (u'<span class="who-chip">Post-stroke &amp; cognitive rehab programs</span>',
     u'<span class="who-chip">Programs alongside rehabilitation teams</span>', 1),

    # ============ C. the two statistics ====================================
    # 73/42 could not be confirmed from any accessible source; the study's
    # reported effect ("almost twice as likely") can be.
    (u'      <div class="stat-big">73%</div>\n'
     u'      <div class="stat-text">of stroke patients who completed '
     u'simulator-based training passed their official pre-driving assessment, '
     u'vs. 42% in a cognitive-only control group.</div>\n'
     u'      <div class="stat-note">* Akinwuntan et al., Neurology (2005)</div>',
     u'      <div class="stat-big">2x</div>\n'
     u'      <div class="stat-text">In a randomized trial of 83 stroke patients, '
     u'those given five weeks of simulator training were close to twice as '
     u'likely to pass an official on-road evaluation as those given '
     u'driving-related cognitive tasks instead.</div>\n'
     u'      <div class="stat-note">* Akinwuntan et al., Neurology (2005)</div>',
     1),

    # The review said the opposite of what this card claimed it said.
    (u'      <div class="stat-big">~33%</div>\n'
     u'      <div class="stat-text">of stroke survivors need structured driving '
     u'rehabilitation before safely returning to the road.</div>\n'
     u'      <div class="stat-note">** George et al., Cochrane Review (2014)</div>',
     u'      <div class="stat-big">4</div>\n'
     u'      <div class="stat-text">trials and 245 participants were all a 2014 '
     u'Cochrane review could find. It concluded there was insufficient evidence '
     u'to say whether driving rehabilitation improves on-road driving skill '
     u'after stroke. We would rather show you that than leave it out.</div>\n'
     u'      <div class="stat-note">** George et al., Cochrane Review (2014)</div>',
     1),

    (u'We’re not making these claims up ' + EM + u' they’re rooted in '
     u'decades of clinical research. A few of the studies behind what we do:', u'', 0),
    (u"We're not making these claims up " + EM + u" they're rooted in decades of "
     u"clinical research. A few of the studies behind what we do:",
     u'Published research on simulator training in older adults and stroke '
     u'survivors. The findings are mixed, and they describe the studies below, '
     u'not results Academy promises.', 1),

    # ============ D. FAQ and scope =========================================
    (u'For early-stage cognitive decline (MCI, mild dementia), many participants '
     u'do very well and research supports benefits.',
     u'For early-stage cognitive decline, many participants take part '
     u'comfortably. Whether it suits a particular person is a decision for them, '
     u'their family and their care team.', 2),

    (u'<strong>A note on scope:</strong> Academy Sim Racing provides simulator '
     u'experiences and structured programs ' + EM + u' we are not a medical '
     u'provider. Clinical outcomes depend on individual health, program design, '
     u'and the involvement of qualified healthcare professionals. We’re '
     u'happy to partner with your facility’s clinical team.', u'', 0),
    (u"<strong>A note on scope:</strong> Academy Sim Racing provides simulator "
     u"experiences and structured programs " + EM + u" we are not a medical "
     u"provider. Clinical outcomes depend on individual health, program design, "
     u"and the involvement of qualified healthcare professionals. We're happy to "
     u"partner with your facility's clinical team.",
     u'<strong>A note on scope:</strong> Academy Sim Racing provides simulator '
     u'experiences and structured programs. We are not a medical provider. We do '
     u'not assess, diagnose or treat any condition, and nothing on this page is '
     u'medical advice or a predicted result. Any clinical decision belongs to '
     u'the participant and their own healthcare professionals, and we are happy '
     u'to work alongside your clinical team.', 1),

    # ============ E. metadata ==============================================
    (u'Cognitive, physical, and social benefits ' + EM + u' fully staffed, '
     u'wheelchair accessible.',
     u'Fully staffed and wheelchair accessible.', 1),
    (u'Cognitive, physical & social benefits.', u'Fully staffed sessions.', 1),
    (u'Cognitive, physical, and social benefits delivered through fully staffed, '
     u'wheelchair-accessible sessions.',
     u'Fully staffed, wheelchair-accessible simulator sessions.', 1),

    # ============ F. second review pass ====================================
    # "programs for ... post-stroke recovery" reads as Academy delivering the
    # recovery, which the same page then disclaims. Academy runs sessions
    # ALONGSIDE somebody else's program. Five places, including the meta
    # description, the og description, the JSON-LD and the footer, so a
    # sentence-level fix in the hero alone would have left four contradictions
    # in place.
    (u'rehab, and post-stroke recovery',
     u'rehab, and alongside post-stroke recovery programs', 3),
    (u'rehabilitation centers, and post-stroke recovery',
     u'rehabilitation centers, and alongside post-stroke recovery programs', 1),
    (u'From retirement community events to post-stroke recovery,',
     u'From retirement community events to sessions alongside post-stroke '
     u'recovery programs,', 1),

    # "asks" framed the offer as a burden; "engages" keeps the commercial
    # warmth without promising a result.
    (u'<h2 class="h2">THREE THINGS IT ASKS AT ONCE</h2>',
     u'<h2 class="h2">THREE THINGS IT ENGAGES AT ONCE</h2>', 1),
    (u'Driving asks for attention, judgement and coordination at the same time,',
     u'Driving engages attention, judgement and coordination at the same time,', 1),

    # "gentle" characterises the movement as therapeutic; "throughout" promises
    # something about how a person will behave for a whole session.
    (u'gentle, repeatable movement with no on-road exposure.',
     u'controlled, repeatable movement with no on-road exposure.', 1),
    (u'<li>Seated throughout, with no on-road exposure</li>',
     u'<li>Seated, with no on-road exposure</li>', 1),
    (u'exposure, and participants stay seated and supervised throughout.',
     u'exposure, participants are seated, and staff stay alongside them.', 2),

    # An "insufficient evidence" number, stated flatly, reads as an admission
    # rather than as candour. Same fact, framed as why we are telling you.
    (u'      <div class="stat-text">trials and 245 participants were all a 2014 '
     u'Cochrane review could find. It concluded there was insufficient evidence '
     u'to say whether driving rehabilitation improves on-road driving skill '
     u'after stroke. We would rather show you that than leave it out.</div>',
     u'      <div class="stat-text">trials, and 245 participants, were all a 2014 '
     u'Cochrane review could find on driving rehabilitation after stroke, and it '
     u'called the results inconclusive. The evidence base is genuinely small. We '
     u'would rather tell you that than quote a number at you.</div>', 1),

    # The same unverified 73/42 split also lived in the research card, so
    # removing it from the stat card alone would have left the page quoting
    # two different versions of one study against itself.
    (u'83 stroke patients randomized to simulator training or cognitive therapy. '
     u'73% of the simulator group passed their official pre-driving assessment '
     u'compared with 42% in the control group. Published in Neurology.',
     u'83 stroke patients randomized to five weeks of simulator training or to '
     u'driving-related cognitive tasks. The simulator group was close to twice '
     u'as likely to pass an official on-road evaluation. Published in Neurology.',
     1),
]

# Outcome verb + health noun, the rule health_audit.py enforces on every page
# built for this property. The homepage was never run through it.
BANNED = re.compile(
    r'\b(improv\w*|boost\w*|enhanc\w*|restor\w*|sharpen\w*|strengthen\w*|'
    r'reduc\w*|combat\w*|prevent\w*|treat\w*|cure\w*|heal\w*)\b[^.<>]{0,40}\b'
    r'(cognition|cognitive|memory|brain|mobility|balance|health|depression|'
    r'dementia|MCI|attention|executive function|reaction time)\b', re.I)
ABSOLUTE = re.compile(
    r'zero (?:fall|risk)|no risk of|risk[- ]free|clinically proven|'
    r'reduces the risk of|helps with dementia|guarantee', re.I)


def strip_code(html):
    return re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.S)


def visible(html):
    """Prose Academy asserts in its own voice.

    The research cards are deliberately excluded. Their subject is a published
    study, not Academy, and one of them is a paper's actual title ("Can
    driving-simulator training enhance visual attention, cognition, and physical
    functioning in older adults?"). The audit asks for research to be framed AS
    research, so accurately summarising a finding there is the goal, not a
    violation. The rule being enforced is narrower than "never use these words":
    it is "never promise these as an Academy outcome".
    """
    t = strip_code(html)
    t = re.sub(r'<div class="research-card">.*?</div>\s*</div>', ' ', t, flags=re.S)
    t = re.sub(r'<div class="research-(?:tag|title|desc)">.*?</div>', ' ', t, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', t)


def main():
    h = io.open(SRC, encoding='utf-8').read()
    applied = 0
    already = []
    for old, new, want in EDITS:
        got = h.count(old)
        if want == 0:                      # optional apostrophe variant
            if got:
                h = h.replace(old, new)
                applied += got
            continue
        if got == 0:
            # ALREADY APPLIED, not missing. This is a one-time copy migration and its edits
            # have since been folded into source/ by hand, in different words -- the same
            # thing that happened to driver, which was solved by retiring its fixers in
            # favour of stage_flat_pages.py (see build_all.py's STEPS comments). 11 of the 41
            # entries here are now in that state, and several chain (one edit's `new` is a
            # later edit's `old`), so the first one to go stale failed the whole build.
            # Zero occurrences means the migration is done. A WRONG COUNT still fails below,
            # because that means real drift rather than completion.
            # THE GATE FOR CLAIMS IS health_audit.py's FORBIDDEN list, not this script.
            already.append(' '.join(old.split())[:72])
            continue
        if got != want:
            print('  !! expected %d, found %d for: %r' % (want, got, old[:80]))
            return 1
        h = h.replace(old, new)
        applied += got
        print('  ok  x%d  %s' % (got, ' '.join(old.split())[:72]))

    if already:
        print('\n  %d edit(s) already applied in source/ (migration complete for these):'
              % len(already))
        for a in already[:4]:
            print('     - %s' % a)
        if len(already) > 4:
            print('     ... and %d more' % (len(already) - 4))
    print('\n  %d replacements applied' % applied)

    # ---- gates -------------------------------------------------------------
    fail = False
    text = visible(h)
    for pat, label in ((BANNED, 'outcome verb + health noun'),
                       (ABSOLUTE, 'absolute safety/medical claim')):
        for m in pat.finditer(text):
            print('  !! %s still present: %r'
                  % (label, ' '.join(text[max(0, m.start() - 60):m.end() + 40].split())))
            fail = True
    # the same rules must hold inside the FAQ/structured data
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
                         h, flags=re.S):
        for pat, label in ((BANNED, 'outcome verb + health noun'),
                           (ABSOLUTE, 'absolute safety/medical claim')):
            for mm in pat.finditer(m.group(1)):
                print('  !! %s in JSON-LD: %r' % (label, mm.group(0)))
                fail = True
    if 'A note on scope' not in h:
        print('  !! scope disclaimer missing'); fail = True
    markup = strip_code(h)      # a <form> inside a JS comment is not a tag
    if markup.count('<form') != markup.count('</form>'):
        print('  !! unbalanced form tags'); fail = True
    if 'data-netlify="true"' not in h or 'netlify-honeypot' not in h:
        print('  !! netlify form attributes lost'); fail = True

    if fail:
        return 1
    if not os.path.isdir(DST):
        os.makedirs(DST)
    out = os.path.join(DST, 'index.html')
    io.open(out, 'w', encoding='utf-8', newline='').write(h)
    print('  clean. wrote %s (%d bytes)' % (out, len(h.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Convert British spelling and idiom to American across the pages I wrote.

Malik's pre-existing pages use American spelling throughout (tire, curb,
center, organizer, practice, color). Mine used British, on sites selling to
Florida. Codex spotted the idiom ("stag", "lifts", "marquees", "car parks");
the spelling is the same defect one layer down.

Only text outside <style> and <script> is touched, so CSS properties like
color: and text-align:center are never rewritten.
"""
import io, os, re, sys

TARGETS = sys.argv[1:]

WORDS = [
    # spelling
    (r'\btyres\b', 'tires'), (r'\btyre\b', 'tire'),
    (r'\bTyres\b', 'Tires'), (r'\bTyre\b', 'Tire'),
    (r'\bkerbs\b', 'curbs'), (r'\bkerb\b', 'curb'),
    (r'\bKerbs\b', 'Curbs'), (r'\bKerb\b', 'Curb'),
    (r'\bpractise\b', 'practice'), (r'\bpractising\b', 'practicing'),
    (r'\bPractise\b', 'Practice'), (r'\bPractising\b', 'Practicing'),
    (r'\bcentres\b', 'centers'), (r'\bcentre\b', 'center'),
    (r'\bCentres\b', 'Centers'), (r'\bCentre\b', 'Center'),
    (r'\borganisers\b', 'organizers'), (r'\borganiser\b', 'organizer'),
    (r'\bOrganisers\b', 'Organizers'), (r'\bOrganiser\b', 'Organizer'),
    (r'\borganised\b', 'organized'), (r'\borganise\b', 'organize'),
    (r'\bcolours\b', 'colors'), (r'\bcolour\b', 'color'),
    (r'\bfavours\b', 'favors'), (r'\bfavour\b', 'favor'),
    (r'\bfavourite\b', 'favorite'), (r'\bfavourites\b', 'favorites'),
    (r'\bmetres\b', 'meters'), (r'\bmetre\b', 'meter'),
    (r'\bprogramme\b', 'program'), (r'\bprogrammes\b', 'programs'),
    (r'\bProgramme\b', 'Program'), (r'\bProgrammes\b', 'Programs'),
    (r'\brealise\b', 'realize'), (r'\brecognise\b', 'recognize'),
    (r'\bcustomised\b', 'customized'), (r'\bcustomise\b', 'customize'),
    (r'\boptimise\b', 'optimize'), (r'\bprioritise\b', 'prioritize'),
    (r'\bspecialise\b', 'specialize'), (r'\banalyse\b', 'analyze'),
    (r'\bbehaviour\b', 'behavior'), (r'\bneighbourhoods\b', 'neighborhoods'),
    (r'\bneighbourhood\b', 'neighborhood'),
    (r'\bapologise\b', 'apologize'), (r'\bemphasise\b', 'emphasize'),
    (r'\bmanoeuvre\b', 'maneuver'), (r'\blitre\b', 'liter'),
    (r'\bdefence\b', 'defense'), (r'\blicence\b', 'license'),
    (r'\bstorey\b', 'story'), (r'\bgrey\b', 'gray'),
    (r'\btravelling\b', 'traveling'), (r'\bTravelling\b', 'Traveling'),
    (r'\borganisations\b', 'organizations'), (r'\borganisation\b', 'organization'),
    (r'\bOrganisations\b', 'Organizations'), (r'\bOrganisation\b', 'Organization'),
    (r'\bmaximises\b', 'maximizes'), (r'\bmaximised\b', 'maximized'),
    (r'\bmaximise\b', 'maximize'), (r'\bMaximise\b', 'Maximize'),
    (r'\bcentrepiece\b', 'centerpiece'), (r'\bcentrepieces\b', 'centerpieces'),
    (r'\bCentrepiece\b', 'Centerpiece'), (r'\bCentrepieces\b', 'Centerpieces'),
    (r'\brecognisable\b', 'recognizable'), (r'\bRecognisable\b', 'Recognizable'),
    (r'\blabour\b', 'labor'), (r'\bLabour\b', 'Labor'),
    # idiom
    (r'\bwhilst\b', 'while'), (r'\bamongst\b', 'among'),
    (r'\bcar parks\b', 'parking lots'), (r'\bcar park\b', 'parking lot'),
    (r'\bmarquees\b', 'event tents'), (r'\bmarquee\b', 'event tent'),
    (r'\bMarquees\b', 'Event tents'),
    (r'\brun-up to the holidays\b', 'lead-up to the holidays'),
    (r'\bstag and bachelorette\b', 'bachelor and bachelorette'),
    (r'\bBACHELOR AND BACHELORETTE\b', 'BACHELOR AND BACHELORETTE'),
    (r'\bstag\b', 'bachelor'), (r'\bStag\b', 'Bachelor'),
]

SPLIT = re.compile(r'(<style[\s\S]*?</style>|<script[\s\S]*?</script>|<!--[\s\S]*?-->)')


def convert(html):
    parts = SPLIT.split(html)
    n = 0
    for i, seg in enumerate(parts):
        if SPLIT.match(seg or ''):
            continue          # leave CSS, JS and comments alone
        for pat, rep in WORDS:
            seg, k = re.subn(pat, rep, seg)
            n += k
        parts[i] = seg
    return ''.join(parts), n


total = 0
for target in TARGETS:
    files = []
    if os.path.isfile(target):
        files = [target]
    else:
        for root, _, fs in os.walk(target):
            for f in fs:
                if f.endswith(('.html', '.py', '.css')):
                    files.append(os.path.join(root, f))
    files.sort()
    for p in files:
        s = io.open(p, encoding='utf-8', newline='').read()
        out, n = convert(s)
        if n:
            io.open(p, 'w', encoding='utf-8', newline='').write(out)
            print('  %-58s %d' % (os.path.relpath(p, os.path.dirname(target) or '.'), n))
            total += n
print('  --- %d conversions ---' % total)

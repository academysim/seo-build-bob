# Full state verification across every surface touched this session.
# Public endpoints only, so it can be re-run any time without credentials.
import json, re, sys, urllib.request, datetime

BOOK = "https://booking.academysim.com"
LOUNGE = "https://lounge.academysim.com"
P = F = 0
FAILS = []


def get(url, raw=False, timeout=45):
    req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read().decode("utf-8", "replace")
    return b if raw else json.loads(b)


def code(url):
    try:
        req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def ck(name, got, want):
    global P, F
    ok = got == want
    if ok:
        P += 1
    else:
        F += 1
        FAILS.append("%s: got %r want %r" % (name, got, want))
    print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, "" if ok else "got %r want %r" % (got, want)))


def hdr(t):
    print("\n" + t)
    print("-" * 74)


# ============================================================ booking site
hdr("BOOKING SITE — build identity")
bj = get(BOOK + "/js/booking.js", raw=True)
aj = get(BOOK + "/js/admin.js", raw=True)
ix = get(BOOK + "/index.html", raw=True)
ck("booking.js build marker", "2026-08-28-v15-auto-walkin" in bj, True)
ck("admin.js build marker", "2026-08-28-v9-auto-walkin" in aj, True)
ck("index.html cache buster ?v=20260828a", "v=20260828a" in ix, True)
ck("no stale 20260814 buster", "20260814" in ix, False)
ck("summary coaching upsell still present", "id=\"coaching-upsell\"" in bj, True)
ck("client short-session pricing present", "function shortSessionPriceCents" in bj, True)

hdr("BOOKING SITE — endpoints")
for e in ["classes", "addons", "rigs", "bootstrap", "promotions", "events"]:
    ck("/api/%s responds 200" % e, code("%s/api/%s" % (BOOK, e)), 200)
ck("/api/lead-intake 404 (site separation)", code(BOOK + "/api/lead-intake"), 404)
ck("admin.html 200", code(BOOK + "/admin.html"), 200)

hdr("BOOKING SITE — availability matrix (28 cells)")
DAYS = [("2026-08-30", "Sun", 18), ("2026-08-31", "Mon", 21), ("2026-09-01", "Tue", None),
        ("2026-09-02", "Wed", 21), ("2026-09-03", "Thu", 21), ("2026-09-04", "Fri", 22),
        ("2026-09-05", "Sat", 22)]
WALKIN = {"Sun", "Mon", "Wed", "Thu"}


def et(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return t.astimezone(datetime.timezone(datetime.timedelta(hours=-4)))


bad = 0
for date, dow, close in DAYS:
    row = []
    for d in [30, 60, 120, 240]:
        r = get("%s/api/availability?date=%s&duration=%d" % (BOOK, date, d))
        n = len(r.get("slots", []))
        wins = r.get("walkin_windows", [])
        row.append("%d:%d" % (d, n))
        if close is None:
            ok = n == 0
        elif d == 30 and dow in WALKIN:
            ok = n == 0 if not wins else True
        else:
            ok = n > 0
        if n and close is not None:
            last = et(r["slots"][-1]["end"])
            if last.hour * 60 + last.minute > close * 60:
                ok = False
        if not ok:
            bad += 1
            FAILS.append("%s %s d=%d n=%d" % (date, dow, d, n))
    print("    %s %-4s  %s" % (date, dow, "  ".join(row)))
ck("all 28 day/duration cells behave correctly", bad, 0)

hdr("BOOKING SITE — the hole that was closed")
ck("Mon 30-min refused (was 18 slots pre-v15)",
   len(get(BOOK + "/api/availability?date=2026-08-31&duration=30")["slots"]), 0)
ck("Mon 60-min still sells",
   len(get(BOOK + "/api/availability?date=2026-08-31&duration=60")["slots"]), 17)
ck("Fri 30-min still sells (unchanged)",
   len(get(BOOK + "/api/availability?date=2026-09-04&duration=30")["slots"]), 16)
ck("Tue closed at every duration",
   sum(len(get(BOOK + "/api/availability?date=2026-09-01&duration=%d" % d)["slots"]) for d in [30, 60, 120]), 0)

hdr("BOOKING SITE — pricing + catalogue")
boot = get(BOOK + "/api/bootstrap")
st = boot["settings"]
cls = get(BOOK + "/api/classes")
ck("short_session_pct = 60", st.get("short_session_pct"), 60)
ck("walkin_min_duration_minutes = 30", st.get("walkin_min_duration_minutes"), 30)
ck("auto_walkin_enabled", st.get("auto_walkin_enabled"), True)
ck("auto_walkin_trail_minutes = 60", st.get("auto_walkin_trail_minutes"), 60)
ck("walk_in_off_until is null", st.get("walk_in_off_until"), None)
ck("no per-class short-session overrides",
   [c["name"] for c in cls if c.get("short_session_price_cents")], [])
ck("8 classes live", len(cls), 8)
ck("rookie-session NOT public", any(c["slug"] == "rookie-session" for c in cls), False)
for slug, name in [("manual-cockpit", "Manual Cockpit"), ("learn-manual", "Learn Manual")]:
    c = [x for x in cls if x["slug"] == slug][0]
    ck("%s rigs = 4,5,6,8" % name, sorted(c.get("member_rig_ids") or []), [4, 5, 6, 8])
rates = {c["name"]: c["hourly_rate_cents"] for c in cls}
for n, hr, half in [("Single Race Rig", 4000, 2400), ("Pro Cockpit", 5000, 3000),
                    ("Manual Cockpit", 5000, 3000), ("Motion GT", 6000, 3600)]:
    ck("%s $%d/hr -> 30min $%d" % (n, hr / 100, half / 100),
       (rates.get(n), round(rates.get(n, 0) * 0.6)), (hr, half))

hdr("BOOKING SITE — coaching copy")
ad = get(BOOK + "/api/addons")
basic = [a for a in ad if a["name"] == "Basic Coaching"][0]
ck("Basic Coaching is $40", basic["price_cents"], 4000)
ck("new copy live (says setup is included)", "come with every booking" in basic["description"], True)
ck("old overlapping copy gone", "make sure you're having fun" in basic["description"], False)
ck("all 4 coaching rows describe a whole session",
   sum(1 for a in ad if "oaching" in a["name"] and "whole session" in a["description"]), 4)

# ============================================================ lounge site
hdr("LOUNGE SITE")
lg = get(LOUNGE + "/", raw=True)
for label, pat, want in [("$249 present", "249", True), ("$449 present", "449", True),
                         ("$300 present", "300", True), ("$549 present", "549", True),
                         ("weekend caveat x5", None, 5)]:
    if pat is None:
        ck(label, lg.count("Friday and Saturday"), want)
    else:
        ck(label, pat in lg, want)
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', lg, re.S)
ck("2 JSON-LD blocks", len(blocks), 2)
parsed = []
for b in blocks:
    try:
        parsed.append(json.loads(b))
    except Exception as e:
        FAILS.append("JSON-LD parse: %s" % e)
ck("both JSON-LD blocks parse", len(parsed), 2)
ck("LocalBusiness + FAQPage present",
   sorted(d.get("@type", "?") for d in parsed), ["FAQPage", "LocalBusiness"])
lb = [d for d in parsed if d.get("@type") == "LocalBusiness"]
ck("LocalBusiness has sameAs", bool(lb and lb[0].get("sameAs")), True)
ck("LocalBusiness has priceRange", bool(lb and lb[0].get("priceRange")), True)
ck("LocalBusiness has postalCode", bool(lb and lb[0].get("address", {}).get("postalCode")), True)
hours = lb[0].get("openingHoursSpecification", []) if lb else []
ck("openingHoursSpecification present", len(hours) > 0, True)
ck("Tuesday absent from schema (closed)",
   any("Tuesday" in str(h.get("dayOfWeek")) for h in hours), False)
sun = [h for h in hours if "Sunday" in str(h.get("dayOfWeek"))]
ck("lounge schema Sunday = 12:00-18:00",
   (sun[0]["opens"], sun[0]["closes"]) if sun else None, ("12:00", "18:00"))
for u in ["/tracks/sebring/", "/og-image.jpg", "/sitemap.xml", "/robots.txt", "/favicon.svg"]:
    ck("lounge %s 200" % u, code(LOUNGE + u), 200)

print("\n" + "=" * 74)
print("  %d passed, %d failed" % (P, F))
if FAILS:
    print("\n  FAILURES:")
    for x in FAILS:
        print("   -", x)
print("=" * 74)
sys.exit(1 if F else 0)

# Independent live probe of the deployed rules, so the agents' findings can be
# cross-checked rather than believed.
import json, urllib.request, datetime, sys

BASE = "https://booking.academysim.com"
DAYS = [
    ("2026-08-30", "Sun", 12, 18), ("2026-08-31", "Mon", 12, 21),
    ("2026-09-01", "Tue", None, None), ("2026-09-02", "Wed", 12, 21),
    ("2026-09-03", "Thu", 12, 21), ("2026-09-04", "Fri", 14, 22),
    ("2026-09-05", "Sat", 14, 22),
]
DURS = [30, 60, 120, 240]
WALKIN_DAYS = {"Sun", "Mon", "Wed", "Thu"}


def get(url):
    with urllib.request.urlopen(url, timeout=40) as r:
        return json.loads(r.read().decode())


def et(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return t.astimezone(datetime.timezone(datetime.timedelta(hours=-4))).strftime("%H:%M")


print("date        day  dur  slots  windows  first..last          verdict")
print("-" * 78)
fails = []
for date, dow, op, cl in DAYS:
    for d in DURS:
        try:
            r = get("%s/api/availability?date=%s&duration=%d" % (BASE, date, d))
        except Exception as e:
            print("  ERROR %s d=%d: %s" % (date, d, e)); fails.append((date, d, str(e))); continue
        n = len(r.get("slots", []))
        w = r.get("walkin_windows", [])
        span = ""
        if n:
            span = "%s..%s" % (et(r["slots"][0]["start"]), et(r["slots"][-1]["end"]))

        # what SHOULD happen
        if op is None:
            want = "0 (closed)"; ok = n == 0
        elif d == 30 and dow in WALKIN_DAYS:
            want = "0 unless a window"; ok = (n == 0) if not w else True
        elif d == 30:
            want = ">0 (Fri/Sat sell 30)"; ok = n > 0
        else:
            want = ">0"; ok = n > 0

        # nothing may ever run past closing
        if n and cl is not None:
            last_end = et(r["slots"][-1]["end"])
            hh, mm = int(last_end[:2]), int(last_end[3:])
            if hh * 60 + mm > cl * 60:
                ok = False; want += " / PAST CLOSE"
        if not ok:
            fails.append((date, d, "n=%d want %s" % (n, want)))
        print("%s %-4s %4d %5d %8d  %-20s %s" % (date, dow, d, n, len(w), span, "ok" if ok else "*** " + want))

print()
print("failures:", len(fails))
for f in fails:
    print("  ", f)

# Rookie Session must not be publicly visible
cls = get(BASE + "/api/classes")
rk = [c for c in cls if c["slug"] == "rookie-session"]
print("\nrookie-session public:", bool(rk), "| classes live:", len(cls))

# manual fleet
for c in cls:
    if c["slug"] in ("manual-cockpit", "learn-manual"):
        print("  %-16s rigs=%s" % (c["name"], sorted(c.get("member_rig_ids") or [])))

# short-session pricing config
b = get(BASE + "/api/bootstrap")
s = b.get("settings", {})
print("\nshort_session_pct:", s.get("short_session_pct"),
      "| walkin_min:", s.get("walkin_min_duration_minutes"),
      "| auto_days:", s.get("auto_walkin_days"),
      "| auto_enabled:", s.get("auto_walkin_enabled"))
sys.exit(1 if fails else 0)

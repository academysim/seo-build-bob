"""Paced demo for the hackathon video. Press Enter to run each step.

Run from the repo root:  python demo_walkthrough.py
Step 2 changes one byte in a shipped page and ALWAYS puts it back, even on Ctrl+C.
"""
import functools, subprocess, sys, time
print = functools.partial(print, flush=True)
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "lounge" / "upload" / "index.html"
CYAN, GREEN, RED, DIM, END = "\033[96m", "\033[92m", "\033[91m", "\033[2m", "\033[0m"


def title(text):
    print(f"\n{CYAN}{'=' * 64}\n  {text}\n{'=' * 64}{END}")


def pause():
    input(f"{DIM}[Enter to continue]{END}")


def run(cmd, timed=False):
    print(f"{GREEN}> {' '.join(cmd)}{END}")
    start = time.perf_counter()
    rc = subprocess.run([sys.executable if c == "python" else c for c in cmd], cwd=ROOT).returncode
    secs = time.perf_counter() - start
    colour = GREEN if rc == 0 else RED
    print(f"{colour}exit {rc}{END}" + (f"   {DIM}({secs:.1f} s){END}" if timed else ""))


def main():
    import os; os.system("")  # turn on colours in a double-clicked Windows console
    title("1. The safety net: every shipped file vs its pre-Bob fingerprint")
    pause()
    run(["python", "shared/tools/verify_baseline.py"], timed=True)

    title("2. Break it on purpose: change ONE character in the live lounge homepage")
    pause()
    original = TARGET.read_bytes()
    try:
        TARGET.write_bytes(original.replace(b"</title>", b"!</title>", 1))
        print(f"{RED}Edited {TARGET.relative_to(ROOT)}: added one '!' to the page title{END}")
        pause()
        run(["python", "shared/tools/verify_baseline.py"])
    finally:
        TARGET.write_bytes(original)
    print(f"{GREEN}Change undone.{END}")
    pause()
    run(["python", "shared/tools/verify_baseline.py"])

    title("3. One home for business details")
    pause()
    print(f"{DIM}shared/tools/constants.py{END}")
    for line in (ROOT / "shared/tools/constants.py").read_text(encoding="utf-8").splitlines():
        if line.startswith(("GA4_TAG", "HOSTS", "    '", "}", "ADDRESS ", "PHONE ", "EMAIL")):
            print("  " + line)
    pause()

    title("4. See what a build would do, without touching anything")
    pause()
    run(["python", "shared/tools/build_all.py", "--dry-run"])

    title("5. All five site audits")
    pause()
    for audit in ["lounge/tools/audit_site.py", "events/tools/events_audit.py",
                  "builds/tools/builds_audit.py", "health/tools/health_audit.py",
                  "driver/tools/driver_audit.py"]:
        run(["python", audit], timed=True)

    title("6. Full test suite")
    pause()
    print(f"{GREEN}> python -m unittest discover -s shared/tests{END}")
    start = time.perf_counter()
    r = subprocess.run([sys.executable, "-W", "ignore", "-m", "unittest", "discover", "-s", "shared/tests"],
                       cwd=ROOT, capture_output=True, text=True)
    secs = time.perf_counter() - start
    # Tests feed deliberately broken fixtures; their "FAILED" chatter is expected. Show the verdict.
    summary = [l for l in r.stderr.splitlines() if l.startswith(("Ran ", "OK", "FAILED"))]
    for line in summary:
        print(line)
    print(f"{GREEN if r.returncode == 0 else RED}exit {r.returncode}{END}   {DIM}({secs:.1f} s){END}")

    title("Done")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        import traceback
        traceback.print_exc()
    input(f"{DIM}[Enter to close]{END}")

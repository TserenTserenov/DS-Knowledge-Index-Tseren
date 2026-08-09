#!/usr/bin/env python3
"""Regression test: concurrent new-post.py invocations must never hand out
the same post_number twice.

Background (WP-502, 2026-08-09): post_number 190, 191, 196 and 197 were each
issued to two different posts. Root cause — next_global_post_number() was
computed by whoever called the script (grep max, +1) with no atomicity
between "read the current max" and "commit a file claiming max+1"; two
agents reading the same snapshot before either had written picked the same
number. The fix wraps allocate-and-write in a single flock() in new-post.py.

This test reproduces that race with real concurrent OS processes (not
threads — flock semantics are process-level, so only real subprocesses
exercise the actual code path that broke in production) against an
isolated copy of the repo, so it never touches real docs/ content.

Run: python3 scripts/test_new_post_race.py
Exit code 0 = all checks passed, non-zero = a check failed (see output).
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POST_NUMBER_RE = re.compile(r"^post_number:\s*(\d+)\s*$", re.MULTILINE)


def make_isolated_repo(tmp_root: Path) -> Path:
    """Copy just enough of the real repo to run new-post.py standalone.

    repo_root() inside new-post.py resolves to the parent of the scripts/
    dir holding the running file, so copying the two script files into
    tmp_root/scripts/ is enough to make tmp_root behave like a repo root —
    no need to clone the (large, unrelated) real docs/ tree.
    """
    scripts_dir = tmp_root / "scripts"
    scripts_dir.mkdir(parents=True)
    for name in ("new-post.py", "_publish_convention.py"):
        shutil.copy2(REPO_ROOT / "scripts" / name, scripts_dir / name)
    (tmp_root / "docs").mkdir()
    return tmp_root


def start_new_post(repo_root: Path, *, date, slug, title,
                   post_number=None) -> subprocess.Popen:
    """Launch (but do not wait for) one new-post.py subprocess."""
    cmd = [sys.executable, str(repo_root / "scripts" / "new-post.py"),
           "--date", date, "--slug", slug, "--title", title,
           "--channels", "club"]
    if post_number is not None:
        cmd += ["--post-number", str(post_number)]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True)


def collect_post_numbers(repo_root: Path):
    """Return [(post_number, path)] for every club file under docs/."""
    found = []
    for path in sorted((repo_root / "docs").glob("**/*-1-club-*.md")):
        m = POST_NUMBER_RE.search(path.read_text(encoding="utf-8"))
        if m:
            found.append((int(m.group(1)), path))
    return found


def scenario_concurrent_auto_allocation(n=12):
    """N parallel agents, each creating a distinct post, none passing
    --post-number (the normal/recommended path). Must yield N distinct,
    contiguous post_number values with zero duplicates — this is the exact
    shape of the race that produced duplicate 190/191/196/197 in prod.
    """
    print(f"\n=== Scenario 1: {n} concurrent auto-allocations ===")
    with tempfile.TemporaryDirectory(prefix="new-post-race-") as tmp:
        repo_root = make_isolated_repo(Path(tmp))
        procs = [
            start_new_post(repo_root, date="2026-08-09", slug=f"race-{i:02d}",
                           title=f"Race post {i}")
            for i in range(n)
        ]
        results = []
        for i, p in enumerate(procs):
            out, err = p.communicate()
            results.append((i, p.returncode, out, err))

        failed = [(i, code, err) for i, code, out, err in results if code != 0]
        for i, code, err in failed:
            print(f"  [race-{i:02d}] exited {code}, stderr: {err.strip()!r}")

        entries = collect_post_numbers(repo_root)
        numbers = sorted(n for n, _ in entries)
        print(f"  processes: {n}, exit_code==0: {n - len(failed)}, "
              f"files with post_number: {len(entries)}")
        print(f"  post_number values (sorted): {numbers}")

        ok = True
        if failed:
            print(f"  FAIL: {len(failed)} subprocess(es) exited non-zero "
                  f"(expected all {n} to succeed, they don't share a number)")
            ok = False
        if len(numbers) != len(set(numbers)):
            dupes = sorted({x for x in numbers if numbers.count(x) > 1})
            print(f"  FAIL: duplicate post_number value(s) found: {dupes}")
            ok = False
        if numbers != list(range(1, n + 1)):
            print(f"  FAIL: expected contiguous 1..{n}, got {numbers}")
            ok = False
        if ok:
            print(f"  PASS: {n}/{n} processes succeeded, "
                  f"{len(set(numbers))} distinct post_number values, "
                  f"contiguous 1..{n}, zero duplicates")
        return ok


def scenario_explicit_collision(n=6):
    """N parallel agents that each independently (and wrongly) pre-computed
    the SAME explicit --post-number and pass it in — the historical failure
    mode (a content plan hands out a number, two agents both use it without
    rechecking the filesystem). Exactly one must win; the rest must fail
    loudly with a clear error, and only one file may end up with that
    number — never a silent duplicate.
    """
    print(f"\n=== Scenario 2: {n} concurrent requests for the SAME "
          f"explicit --post-number ===")
    with tempfile.TemporaryDirectory(prefix="new-post-collision-") as tmp:
        repo_root = make_isolated_repo(Path(tmp))
        procs = [
            start_new_post(repo_root, date="2026-08-09", slug=f"collide-{i:02d}",
                           title=f"Collide post {i}", post_number=42)
            for i in range(n)
        ]
        results = []
        for i, p in enumerate(procs):
            out, err = p.communicate()
            results.append((i, p.returncode, out, err))

        succeeded = [i for i, code, out, err in results if code == 0]
        failed = [(i, err) for i, code, out, err in results if code != 0]
        for i, err in failed:
            tail = err.strip().splitlines()[-1] if err.strip() else ""
            print(f"  [collide-{i:02d}] rejected: {tail!r}")

        entries = collect_post_numbers(repo_root)
        owners = [p for n_, p in entries if n_ == 42]
        print(f"  succeeded: {len(succeeded)}/{n}, rejected: {len(failed)}/{n}, "
              f"files claiming post_number 42: {len(owners)}")

        ok = True
        if len(succeeded) != 1:
            print(f"  FAIL: expected exactly 1 winner, got {len(succeeded)}")
            ok = False
        if len(owners) != 1:
            print(f"  FAIL: expected exactly 1 file with post_number 42, "
                  f"got {len(owners)}: {owners}")
            ok = False
        if len(failed) != n - 1:
            print(f"  FAIL: expected {n - 1} rejections, got {len(failed)}")
            ok = False
        if ok:
            print(f"  PASS: 1 winner, {n - 1} clean rejections (occupancy "
                  f"checked, not silently duplicated), exactly 1 file on disk")
        return ok


def main():
    r1 = scenario_concurrent_auto_allocation(n=12)
    r2 = scenario_explicit_collision(n=6)
    print()
    if r1 and r2:
        print("ALL CHECKS PASSED")
        return 0
    print("SOME CHECKS FAILED — see FAIL lines above")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

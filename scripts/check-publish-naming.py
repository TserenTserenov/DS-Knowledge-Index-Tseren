#!/usr/bin/env python3
"""Guard: validate knowledge-index publication folder names against convention.

Two modes:
  (default)  full scan of docs/{YYYY}/ — report every violation, exit 1 if any.
             Use manually or in CI as a backstop.
  --staged   delta-aware: only check newly ADDED paths in the git index, so a
             commit is blocked only when IT introduces a bad name. Pre-existing
             drift does not block unrelated commits.

Only directories are validated (month folders and post folders) — that is where
the recurring drift happens. Loose service files (week reviews, drafts) follow
looser rules and are left to the author.

Run manually:   python3 scripts/check-publish-naming.py
Pre-commit:     python3 scripts/check-publish-naming.py --staged
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Import the shared convention (sibling module) — single source of truth.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _publish_convention import (  # noqa: E402
    MONTH_BY_NAME, MONTH_DIR_RE, NON_MONTH_DIRS,
    validate_month_dir, validate_post_dir,
)


def repo_root() -> Path:
    """Repo root = parent of the scripts/ directory holding this file."""
    return Path(__file__).resolve().parent.parent


def month_of_dir(month_dirname: str):
    """Real calendar month for a month folder name, or None if not one."""
    m = MONTH_DIR_RE.match(month_dirname)
    if not m:
        return None
    return MONTH_BY_NAME.get(m.group(2))


def scan_full(root: Path):
    """Return [(relative_path, reason)] for every violation under docs/."""
    violations = []
    for year_dir in sorted((root / "docs").glob("[0-9][0-9][0-9][0-9]")):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(p for p in year_dir.iterdir() if p.is_dir()):
            ok, reason = validate_month_dir(month_dir.name)
            if not ok:
                violations.append((month_dir.relative_to(root), reason))
                continue
            if month_dir.name in NON_MONTH_DIRS:
                continue
            parent_month = month_of_dir(month_dir.name)
            for post_dir in sorted(p for p in month_dir.iterdir() if p.is_dir()):
                ok, reason = validate_post_dir(post_dir.name, parent_month)
                if not ok:
                    violations.append((post_dir.relative_to(root), reason))
    return violations


def staged_added_paths():
    """Paths added (A) in the git index, relative to repo root.

    Uses -z (NUL-separated) so non-ASCII paths are returned literally; without
    it git escapes Cyrillic folder names (e.g. "07-июнь"), which silently broke
    path parsing and let bad names through.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A", "-z"],
        capture_output=True, text=True, check=True)
    return [p for p in result.stdout.split("\0") if p]


def scan_staged(root: Path):
    """Validate only month/post folders touched by newly added files."""
    violations = []
    seen = set()
    for rel in staged_added_paths():
        parts = Path(rel).parts
        # Expect docs/{YYYY}/{monthdir}/...
        if len(parts) < 3 or parts[0] != "docs":
            continue
        year, monthdir = parts[1], parts[2]
        if ("month", monthdir) not in seen:
            seen.add(("month", monthdir))
            ok, reason = validate_month_dir(monthdir)
            if not ok:
                violations.append((Path("docs") / year / monthdir, reason))
        # docs/{YYYY}/{monthdir}/{postdir}/file -> validate the post folder
        if len(parts) >= 5:
            postdir = parts[3]
            key = ("post", monthdir, postdir)
            if key not in seen:
                seen.add(key)
                ok, reason = validate_post_dir(postdir, month_of_dir(monthdir))
                if not ok:
                    violations.append(
                        (Path("docs") / year / monthdir / postdir, reason))
    return violations


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Проверка имён публикаций индекса знаний по конвенции.")
    ap.add_argument("--staged", action="store_true",
                    help="Проверять только новые файлы в индексе git (pre-commit)")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    root = repo_root()
    violations = scan_staged(root) if args.staged else scan_full(root)

    if not violations:
        scope = "новые файлы" if args.staged else "docs/"
        print(f"✅ Имена публикаций в норме ({scope}).")
        return 0

    print(f"❌ Нарушений конвенции имён: {len(violations)}")
    for path, reason in violations:
        print(f"   {path}  — {reason}")
    print()
    print("Создавай папки постов через scripts/new-post.py — он считает имена сам.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

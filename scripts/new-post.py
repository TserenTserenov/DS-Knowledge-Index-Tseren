#!/usr/bin/env python3
"""Scaffold a publication folder for the knowledge index, by convention.

This is the single source of truth for folder/file names. Do NOT create post
folders by hand: the month-folder uses REVERSE numbering (13 - month) so the
freshest month sorts to the top on GitHub, while the post folder uses the REAL
calendar month. Computing both by hand is the source of recurring drift
(see CLAUDE.md "3. Формат поста").

Naming produced:
  docs/{YYYY}/{NN}-{month}/{PP}-{MM}-{YYYY-MM-DD}-{slug}/
      {PP}-{MM}-{ch}-{channel}-{YYYY-MM-DD}.md   (one per channel)
where:
  NN = 13 - calendar_month   (reverse, newest month on top)
  MM = calendar_month        (real month)
  PP = next sequential post number within the month (resets monthly)

Usage:
  python3 scripts/new-post.py --date 2026-06-22 --slug my-topic \\
      --title "Название поста" [--audience community] [--channels club,telegram] \\
      [--related-wp 406] [--content-plan WP-406] \\
      [--source-knowledge PACK-personal/PD.METHOD.001] [--dry-run]

post_number allocation (frontmatter "post_number", the historical cross-
channel counter) is automatic and atomic: the script scans every existing
club file for its highest post_number and claims max+1, all under a file
lock (see _allocation_lock below). Do NOT compute it yourself and pass it
in — that "read max elsewhere, then call the script" pattern is exactly
what produced duplicate post_number 190/191/196/197 (two agents each
computed "next" from a snapshot that was already stale by the time either
one wrote a file). --post-number remains available for a deliberate
backfill/override, but the script still validates occupancy under the
same lock and refuses to hand out a number that is already taken.
"""

import argparse
import contextlib
import fcntl
import re
import sys
from datetime import date as date_cls
from pathlib import Path

# Import the shared convention (sibling module) — single source of truth.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _publish_convention import (  # noqa: E402
    CHANNELS, MONTHS_RU, NEW_POST_PREFIX_RE, SLUG_RE, reverse_month_number,
)

# Matches the frontmatter line in any club (source-of-truth) file, new-style
# ("PP-MM-...-1-club-...md") or legacy ("NNN-1-club-...md") naming alike —
# every post's canonical post_number lives there.
POST_NUMBER_RE = re.compile(r"^post_number:\s*(\d+)\s*$", re.MULTILINE)


def repo_root() -> Path:
    """Repo root = parent of the scripts/ directory holding this file."""
    return Path(__file__).resolve().parent.parent


@contextlib.contextmanager
def _allocation_lock(root: Path):
    """Serialize the scan-decide-write critical section across processes.

    Without this, two concurrent invocations (two agents working in
    parallel, or one agent re-run before the first finished) each scan the
    current max PP/post_number, independently compute "next", and only
    then write files — a classic read-then-write race with no atomicity
    in between. flock() turns "scan existing numbers, decide the next one,
    write files claiming it" into one atomic transaction: a second process
    blocks until the first has committed its files to disk, so its own
    scan always sees the first process's claim and computes a different
    number.

    OS-level flock (not a marker/lockfile-exists check) is released
    automatically when the holding process exits, including on a crash —
    so a dead process can never leave a stale lock blocking everyone else.
    """
    lock_path = root / "scripts" / ".new-post.lock"
    with open(lock_path, "a") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def next_post_number(month_dir: Path, mm: str) -> int:
    """Return the next sequential PP within the month (max existing + 1).

    Caller must hold _allocation_lock() — see next_global_post_number for
    why an unlocked scan-then-decide is unsafe under concurrency.
    """
    if not month_dir.is_dir():
        return 1
    used = []
    for child in month_dir.iterdir():
        if not child.is_dir():
            continue
        m = NEW_POST_PREFIX_RE.match(child.name)
        # Only count folders of the same calendar month to be safe.
        if m and m.group(2) == mm:
            used.append(int(m.group(1)))
    return (max(used) + 1) if used else 1


def _all_club_post_numbers(root: Path):
    """Yield (post_number, path) for every club file that declares one."""
    for path in (root / "docs").glob("**/*-1-club-*.md"):
        m = POST_NUMBER_RE.search(path.read_text(encoding="utf-8"))
        if m:
            yield int(m.group(1)), path


def next_global_post_number(root: Path) -> int:
    """Return (highest existing frontmatter post_number across docs/) + 1.

    This is the sole allocator for post_number — see the module docstring
    for why callers must not pre-compute this themselves. Caller must hold
    _allocation_lock().
    """
    highest = max((n for n, _ in _all_club_post_numbers(root)), default=0)
    return highest + 1


def post_number_owner(root: Path, n: int) -> Path | None:
    """Return the club file already using post_number n, or None if free.

    Caller must hold _allocation_lock() for the result to be race-safe.
    """
    for existing_n, path in _all_club_post_numbers(root):
        if existing_n == n:
            return path
    return None


def build_frontmatter(*, title, audience, created, channel, channel_number,
                      post_number, source_post, source_knowledge,
                      content_plan, related_wp) -> str:
    """Render frontmatter matching the contract in CLAUDE.md "Frontmatter"."""
    lines = [
        "---",
        "type: post",
        f'title: "{title}"',
        f"audience: {audience}",
        "status: draft",
        f"created: {created}",
        f"target: {channel}",
        f"channel_number: {channel_number}",
    ]
    if post_number is not None:
        lines.append(f"post_number: {post_number}")
    if source_post:  # adaptations point back at the club source-of-truth
        lines.append(f'source_post: "{source_post}"')
    lines.append(f'source_knowledge: "{source_knowledge}"' if source_knowledge
                 else "source_knowledge: null")
    lines.append("tags: []")
    lines.append(f'content_plan: "{content_plan}"' if content_plan
                 else 'content_plan: ""')
    if related_wp is not None:
        lines.append(f"related_wp: {related_wp}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Скаффолд папки публикации индекса знаний по конвенции.")
    p.add_argument("--date", required=True, help="Дата публикации YYYY-MM-DD")
    p.add_argument("--slug", required=True, help="Английский slug через дефис")
    p.add_argument("--title", required=True, help="Заголовок поста (русский)")
    p.add_argument("--audience", default="community",
                   choices=["wide", "community", "advanced"])
    p.add_argument("--channels", default="club",
                   help="Каналы через запятую (по умолчанию club)")
    p.add_argument("--post-number", type=int, default=None,
                   help="Только для ручного backfill/override — по умолчанию "
                        "номер выделяется сам (сквозной исторический номер, "
                        "frontmatter). Если номер уже занят — ошибка, не "
                        "тихий дубль.")
    p.add_argument("--related-wp", type=int, default=None)
    p.add_argument("--content-plan", default=None, help='Например WP-406')
    p.add_argument("--source-knowledge", default=None)
    p.add_argument("--dry-run", action="store_true",
                   help="Показать, что будет создано, без записи файлов")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    # --- validate inputs ---
    try:
        d = date_cls.fromisoformat(args.date)
    except ValueError:
        print(f"❌ Неверная дата: {args.date!r}. Нужен формат YYYY-MM-DD.",
              file=sys.stderr)
        return 2

    if not SLUG_RE.match(args.slug):
        print(f"❌ slug {args.slug!r} должен быть английским, строчным, через "
              f"дефис (пример: dual-loop-reflexes).", file=sys.stderr)
        return 2

    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    unknown = [c for c in channels if c not in CHANNELS]
    if unknown:
        print(f"❌ Неизвестные каналы: {', '.join(unknown)}. "
              f"Доступны: {', '.join(CHANNELS)}.", file=sys.stderr)
        return 2
    # club is the source-of-truth; keep it first and always present.
    if "club" not in channels:
        channels.insert(0, "club")
    channels = sorted(set(channels), key=lambda c: CHANNELS[c])

    # --- compute names ---
    nn = reverse_month_number(d.month)
    mm = f"{d.month:02d}"
    month_name = MONTHS_RU[d.month]
    root = repo_root()
    month_dir = root / "docs" / str(d.year) / f"{nn:02d}-{month_name}"

    if args.dry_run:
        # Preview only, no lock: nothing is claimed or written, so there is
        # nothing to protect atomically. The previewed post_number is a
        # snapshot and may differ from what a real (locked) run allocates
        # if something else writes a post in between — that is inherent to
        # "preview" and is exactly why the write path below re-scans fresh
        # under the lock instead of trusting this value.
        pp = next_post_number(month_dir, mm)
        post_dir = month_dir / f"{pp:02d}-{mm}-{args.date}-{args.slug}"
        preview_post_number = (args.post_number if args.post_number is not None
                               else next_global_post_number(root))
        club_filename = f"{pp:02d}-{mm}-{CHANNELS['club']}-club-{args.date}.md"
        rel = post_dir.relative_to(root)
        print(f"[dry-run] Папка поста: {rel}/")
        print(f"[dry-run]   месяц: {month_name} → внешний {nn:02d} (обратный), "
              f"календарный {mm}; порядковый в месяце {pp:02d}; "
              f"post_number (превью, не забронирован): {preview_post_number}")
        for ch in channels:
            fname = f"{pp:02d}-{mm}-{CHANNELS[ch]}-{ch}-{args.date}.md"
            print(f"[dry-run]   + {post_dir.relative_to(root)}/{fname}")
        print("[dry-run] Ничего не записано (убери --dry-run для создания).")
        return 0

    # --- allocate + write, atomically ---
    # Everything that reads current post state to decide a number, and
    # everything that writes files claiming that number, happens inside
    # ONE lock acquisition — see _allocation_lock docstring for why the
    # scan and the write cannot be split across the lock boundary.
    with _allocation_lock(root):
        pp = next_post_number(month_dir, mm)
        post_dir = month_dir / f"{pp:02d}-{mm}-{args.date}-{args.slug}"

        if post_dir.exists():
            print(f"❌ Папка уже существует: {post_dir.relative_to(root)}",
                  file=sys.stderr)
            return 1

        if args.post_number is not None:
            owner = post_number_owner(root, args.post_number)
            if owner is not None:
                print(f"❌ post_number {args.post_number} уже занят: "
                      f"{owner.relative_to(root)}. Не вычисляй номер вручную — "
                      f"убери --post-number, скрипт выделит свободный сам.",
                      file=sys.stderr)
                return 1
            post_number = args.post_number
        else:
            post_number = next_global_post_number(root)

        club_filename = f"{pp:02d}-{mm}-{CHANNELS['club']}-club-{args.date}.md"

        # --- plan files ---
        planned = []
        for ch in channels:
            fname = f"{pp:02d}-{mm}-{CHANNELS[ch]}-{ch}-{args.date}.md"
            source_post = None if ch == "club" else club_filename
            content = build_frontmatter(
                title=args.title, audience=args.audience, created=args.date,
                channel=ch, channel_number=CHANNELS[ch],
                post_number=post_number, source_post=source_post,
                source_knowledge=args.source_knowledge,
                content_plan=args.content_plan, related_wp=args.related_wp)
            planned.append((post_dir / fname, content))

        # --- write ---
        post_dir.mkdir(parents=True, exist_ok=False)
        for path, content in planned:
            path.write_text(content, encoding="utf-8")

    rel = post_dir.relative_to(root)
    print(f"✅ Создана папка поста: {rel}/ (post_number: {post_number})")
    for path, _ in planned:
        print(f"   + {path.relative_to(root)}")
    print()
    print("Дальше по Exit Protocol (CLAUDE.md §5):")
    print("  1. Написать club-лонгрид (source-of-truth), затем адаптации")
    print("  2. Обложка: python generate_post_image.py <путь к club .md>")
    print(f"  3. Обновить docs/README.md (строка сверху в месяце «{month_name.capitalize()}»)")
    print("  4. git add docs/ && commit && push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

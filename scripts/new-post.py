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
      [--post-number 165] [--related-wp 406] [--content-plan WP-406] \\
      [--source-knowledge PACK-personal/PD.METHOD.001] [--dry-run]
"""

import argparse
import sys
from datetime import date as date_cls
from pathlib import Path

# Import the shared convention (sibling module) — single source of truth.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _publish_convention import (  # noqa: E402
    CHANNELS, MONTHS_RU, NEW_POST_PREFIX_RE, SLUG_RE, reverse_month_number,
)


def repo_root() -> Path:
    """Repo root = parent of the scripts/ directory holding this file."""
    return Path(__file__).resolve().parent.parent


def next_post_number(month_dir: Path, mm: str) -> int:
    """Return the next sequential PP within the month (max existing + 1)."""
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
                   help="Сквозной исторический номер поста (frontmatter)")
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
    pp = next_post_number(month_dir, mm)
    post_dir = month_dir / f"{pp:02d}-{mm}-{args.date}-{args.slug}"

    if post_dir.exists():
        print(f"❌ Папка уже существует: {post_dir.relative_to(root)}",
              file=sys.stderr)
        return 1

    club_filename = f"{pp:02d}-{mm}-{CHANNELS['club']}-club-{args.date}.md"

    # --- plan files ---
    planned = []
    for ch in channels:
        fname = f"{pp:02d}-{mm}-{CHANNELS[ch]}-{ch}-{args.date}.md"
        source_post = None if ch == "club" else club_filename
        content = build_frontmatter(
            title=args.title, audience=args.audience, created=args.date,
            channel=ch, channel_number=CHANNELS[ch],
            post_number=args.post_number, source_post=source_post,
            source_knowledge=args.source_knowledge,
            content_plan=args.content_plan, related_wp=args.related_wp)
        planned.append((post_dir / fname, content))

    rel = post_dir.relative_to(root)
    if args.dry_run:
        print(f"[dry-run] Папка поста: {rel}/")
        print(f"[dry-run]   месяц: {month_name} → внешний {nn:02d} (обратный), "
              f"календарный {mm}; порядковый в месяце {pp:02d}")
        for path, _ in planned:
            print(f"[dry-run]   + {path.relative_to(root)}")
        print("[dry-run] Ничего не записано (убери --dry-run для создания).")
        return 0

    # --- write ---
    post_dir.mkdir(parents=True, exist_ok=False)
    for path, content in planned:
        path.write_text(content, encoding="utf-8")

    print(f"✅ Создана папка поста: {rel}/")
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

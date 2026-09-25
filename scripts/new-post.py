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
      [--source-knowledge PACK-personal/PD.METHOD.001] \\
      --draft-id UUID --post-number NUMBER [--dry-run]

Reserve the historical cross-channel post_number through personal_new_post
FIRST, retaining the same draft_id UUID for retries (WP-560 Ф12). Real writes
require that UUID and the returned number. The existing authenticated gh CLI
reads docs/_allocator-log.jsonl from an immutable commit on origin's current
default branch; missing or ambiguous reservations stop creation. No local
allocator or manual-number fallback exists. The local lock still protects
monthly folder numbering and checks for existing files. Replays are refused
with the existing path, without overwriting content.

--dry-run requires an explicit positive --post-number but needs neither gh
nor a reservation. Its output is an unverified preview, never a reservation.
"""

import argparse
import base64
import binascii
import contextlib
import fcntl
import json
import re
import subprocess
import sys
from datetime import date as date_cls
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from uuid import UUID

# Import the shared convention (sibling module) — single source of truth.
# Validation failures and dry-run must not create even a bytecode cache.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _publish_convention import (  # noqa: E402
    CHANNELS, MONTHS_RU, NEW_POST_PREFIX_RE, SLUG_RE, reverse_month_number,
)

# Matches the frontmatter line in any club (source-of-truth) file, new-style
# ("PP-MM-...-1-club-...md") or legacy ("NNN-1-club-...md") naming alike —
# every post's canonical post_number lives there.
POST_NUMBER_RE = re.compile(r"^post_number:\s*(\d+)\s*$", re.MULTILINE)
DRAFT_ID_RE = re.compile(r"^draft_id:\s*[\"']?([0-9a-fA-F-]{36})[\"']?\s*$", re.MULTILINE)
UUID_RE = re.compile(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}")
MAX_POST_NUMBER = 2**53 - 1


class ReservationError(ValueError):
    """A reservation could not be verified; no publication may be written."""


def repo_root() -> Path:
    """Repo root = parent of the scripts/ directory holding this file."""
    return Path(__file__).resolve().parent.parent


def canonical_draft_id(value: str) -> str:
    if not isinstance(value, str) or not UUID_RE.fullmatch(value):
        raise ReservationError("draft_id должен быть UUID в формате 8-4-4-4-12.")
    return str(UUID(value))


def read_command(args: list[str], root: Path) -> str:
    """Keep CLI diagnostics private: they may contain authentication data."""
    try:
        result = subprocess.run(args, cwd=root, capture_output=True, text=True,
                                timeout=30, check=True)
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise ReservationError(
            "Не удалось прочитать резервацию. Нужны доступный origin на GitHub, "
            "сеть и авторизованный gh; проверьте gh auth status.") from exc
    return result.stdout


def github_json(root: Path, endpoint: str) -> dict:
    response = read_command([
        "gh", "api", "--hostname", "github.com", "--method", "GET",
        "-H", "Accept: application/vnd.github+json",
        "-H", "Cache-Control: no-cache", endpoint,
    ], root)
    try:
        payload = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ReservationError("GitHub вернул некорректный ответ.") from exc
    if not isinstance(payload, dict):
        raise ReservationError("GitHub вернул некорректный ответ.")
    return payload


def remote_allocator_log(root: Path) -> str:
    remote = read_command(["git", "remote", "get-url", "origin"], root).strip()
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
        r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?", remote)
    if not match:
        raise ReservationError("origin должен указывать на репозиторий github.com.")
    endpoint = f"repos/{match.group(1)}"
    branch = github_json(root, endpoint).get("default_branch")
    if not isinstance(branch, str) or not branch:
        raise ReservationError("Не удалось определить основную ветку GitHub.")
    snapshot = github_json(root, f"{endpoint}/commits/{quote(branch, safe='')}")
    sha = snapshot.get("sha")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ReservationError("Не удалось определить снимок основной ветки GitHub.")
    payload = github_json(root, f"{endpoint}/contents/docs/_allocator-log.jsonl?ref={sha}")
    content = payload.get("content")
    if (payload.get("type") != "file" or payload.get("encoding") != "base64"
            or not isinstance(content, str)):
        raise ReservationError("GitHub не вернул полный журнал резерваций.")
    try:
        return base64.b64decode("".join(content.split()), validate=True).decode("utf-8")
    except (binascii.Error, UnicodeError, ValueError) as exc:
        raise ReservationError("Не удалось прочитать журнал резерваций GitHub.") from exc


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReservationError("Журнал резерваций содержит повторяющееся поле.")
        result[key] = value
    return result


def verify_reservation(log: str, draft_id: str, post_number: int) -> None:
    """Validate the whole ledger, including conflicts unrelated to this draft."""
    reservations = {}
    used_numbers = set()
    for line in log.splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line, object_pairs_hook=unique_json_object)
            if not isinstance(entry, dict) or entry.get("artifact_type") != "post":
                raise ValueError("invalid artifact type")
            entry_id = canonical_draft_id(entry.get("draft_id"))
            number = entry.get("post_number")
            if type(number) is not int or not 1 <= number <= MAX_POST_NUMBER:
                raise ValueError("invalid post number")
            timestamp = entry.get("timestamp")
            if not isinstance(timestamp, str) or "T" not in timestamp:
                raise ValueError("invalid timestamp")
            if datetime.fromisoformat(timestamp.replace("Z", "+00:00")).tzinfo is None:
                raise ValueError("timestamp must include timezone")
        except (ValueError, TypeError) as exc:
            raise ReservationError("Журнал резерваций повреждён; создание остановлено.") from exc
        if entry_id in reservations or number in used_numbers:
            raise ReservationError("Журнал резерваций неоднозначен: повтор UUID или номера.")
        reservations[entry_id] = number
        used_numbers.add(number)
    if reservations.get(draft_id) != post_number:
        raise ReservationError(
            "Пара draft_id и post_number не подтверждена журналом GitHub. "
            "Сначала вызовите personal_new_post с этим UUID и используйте его номер.")


@contextlib.contextmanager
def _allocation_lock(root: Path):
    """Serialize local monthly numbering, ownership checks and file creation.

    Cross-machine post_number reservation belongs to personal_new_post.

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

    Caller must hold _allocation_lock() when creating files.
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


def post_number_owner(root: Path, n: int) -> Path | None:
    """Return the club file already using post_number n, or None if free.

    Caller must hold _allocation_lock() for the result to be race-safe.
    """
    for existing_n, path in _all_club_post_numbers(root):
        if existing_n == n:
            return path
    return None


def draft_owner(root: Path, draft_id: str) -> Path | None:
    for path in (root / "docs").glob("**/*-1-club-*.md"):
        match = DRAFT_ID_RE.search(path.read_text(encoding="utf-8"))
        if match and match.group(1).lower() == draft_id:
            return path
    return None


def build_frontmatter(*, title, audience, created, channel, channel_number,
                      post_number, draft_id, source_post, source_knowledge,
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
        f"draft_id: {draft_id}",
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
    p.add_argument("--post-number", type=int, required=True,
                   help="Сквозной номер из personal_new_post; локального выделения нет.")
    p.add_argument("--draft-id", default=None,
                   help="UUID резервации personal_new_post; обязателен для записи.")
    p.add_argument("--related-wp", type=int, default=None)
    p.add_argument("--content-plan", default=None, help='Например WP-406')
    p.add_argument("--source-knowledge", default=None)
    p.add_argument("--dry-run", action="store_true",
                   help="Показать, что будет создано, без записи файлов")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        if not 1 <= args.post_number <= MAX_POST_NUMBER:
            raise ReservationError(
                "post_number должен быть положительным безопасным целым числом.")
        draft_id = canonical_draft_id(args.draft_id) if args.draft_id is not None else None
        if not args.dry_run and draft_id is None:
            raise ReservationError("Для записи нужен --draft-id UUID из personal_new_post.")
    except ReservationError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2

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
        # Preview does not verify or create a reservation, and never writes.
        pp = next_post_number(month_dir, mm)
        post_dir = month_dir / f"{pp:02d}-{mm}-{args.date}-{args.slug}"
        rel = post_dir.relative_to(root)
        print(f"[dry-run] Папка поста: {rel}/")
        print(f"[dry-run]   месяц: {month_name} → внешний {nn:02d} (обратный), "
              f"календарный {mm}; порядковый в месяце {pp:02d}; "
              f"post_number (превью, резервация не проверена): {args.post_number}")
        for ch in channels:
            fname = f"{pp:02d}-{mm}-{CHANNELS[ch]}-{ch}-{args.date}.md"
            print(f"[dry-run]   + {post_dir.relative_to(root)}/{fname}")
        print("[dry-run] Ничего не записано. Для создания нужны подтверждённые "
              "--draft-id и --post-number из personal_new_post.")
        return 0

    # Fail before even creating the local lock file if verification is unavailable.
    try:
        verify_reservation(remote_allocator_log(root), draft_id, args.post_number)
    except ReservationError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    with _allocation_lock(root):
        pp = next_post_number(month_dir, mm)
        post_dir = month_dir / f"{pp:02d}-{mm}-{args.date}-{args.slug}"

        if post_dir.exists():
            print(f"❌ Папка уже существует: {post_dir.relative_to(root)}",
                  file=sys.stderr)
            return 1

        owner = draft_owner(root, draft_id) or post_number_owner(root, args.post_number)
        if owner is not None:
            print(f"❌ UUID или post_number {args.post_number} уже записан: "
                  f"{owner.relative_to(root)}. Повтор не меняет существующий пост.",
                  file=sys.stderr)
            return 1
        post_number = args.post_number

        club_filename = f"{pp:02d}-{mm}-{CHANNELS['club']}-club-{args.date}.md"

        # --- plan files ---
        planned = []
        for ch in channels:
            fname = f"{pp:02d}-{mm}-{CHANNELS[ch]}-{ch}-{args.date}.md"
            source_post = None if ch == "club" else club_filename
            content = build_frontmatter(
                title=args.title, audience=args.audience, created=args.date,
                channel=ch, channel_number=CHANNELS[ch],
                post_number=post_number, draft_id=draft_id, source_post=source_post,
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
    print("  2. Обновить docs/README.md "
          f"(строка сверху в месяце «{month_name.capitalize()}»)")
    print("  3. Добавить в git только созданные файлы, затем commit и push")
    print("  (Обложка не обязательна и не блокирует status: ready; "
          "генератор — внешний скрипт в DS-IT-systems, см. PROCESSES.md S48 / CLAUDE.md §5)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

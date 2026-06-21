"""Single source of truth for the knowledge-index publication naming convention.

Imported by both new-post.py (scaffold) and check-publish-naming.py (guard) so
the two tools can never drift apart. The whole point of this module is that the
folder/file names are decided in exactly one place.

Convention (see CLAUDE.md "3. Формат поста"):
  docs/{YYYY}/{NN}-{month}/{PP}-{MM}-{YYYY-MM-DD}-{slug}/
where NN = 13 - calendar_month (reverse: newest month sorts to the top on
GitHub), MM = real calendar month, PP = sequential post number within month.
"""

import re

# Channel registry — fixed numbering, see CLAUDE.md "Реестр каналов".
CHANNELS = {
    "club": 1,
    "facebook": 2,
    "linkedin": 3,
    "telegram": 4,
    "tenchat": 5,
    "x": 6,
    "youtube": 7,
    "dzen": 8,
}

# Russian month names in nominative case, as used in directory names.
MONTHS_RU = {
    1: "январь", 2: "февраль", 3: "март", 4: "апрель",
    5: "май", 6: "июнь", 7: "июль", 8: "август",
    9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь",
}
MONTH_BY_NAME = {name: num for num, name in MONTHS_RU.items()}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Month directory: "{NN}-{month}", e.g. "07-июнь".
MONTH_DIR_RE = re.compile(r"^(\d{2})-(.+)$")

# Prefix used by the scaffold to find the next PP within a month.
NEW_POST_PREFIX_RE = re.compile(r"^(\d{2})-(\d{2})-\d{4}-\d{2}-\d{2}-")

# A post folder name is valid if it matches one of these (new + two legacy forms).
NEW_POST_RE = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")     # PP-MM-YYYY-MM-DD-slug
LEGACY_POST_RE = re.compile(r"^\d{3}-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")        # NNN-YYYY-MM-DD-slug
LEGACY_ALT_POST_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}-[a-z0-9-]+$")    # YYYY-MM-DD-NNN-slug
# Service posts/files without a number (week reviews, single notes).
SERVICE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+(?:\.md)?$")

# Month directories that are not month folders and should be skipped.
NON_MONTH_DIRS = {"images"}


def reverse_month_number(month: int) -> int:
    """Reverse index so the newest month sorts first on GitHub (June -> 07)."""
    return 13 - month


def validate_month_dir(name: str):
    """Validate a "docs/{YYYY}/" child. Returns (ok: bool, reason: str)."""
    if name in NON_MONTH_DIRS:
        return True, ""
    m = MONTH_DIR_RE.match(name)
    if not m:
        return False, "не по шаблону {NN}-{месяц}"
    nn, month_name = int(m.group(1)), m.group(2)
    month = MONTH_BY_NAME.get(month_name)
    if month is None:
        return False, f"неизвестный месяц «{month_name}»"
    expected = reverse_month_number(month)
    if nn != expected:
        return False, (f"обратный номер месяца должен быть {expected:02d} "
                       f"(13 − {month}), а стоит {nn:02d}")
    return True, ""


def validate_post_dir(name: str, parent_month: int | None):
    """Validate a post folder name. Returns (ok: bool, reason: str).

    parent_month is the real calendar month of the containing folder, used to
    cross-check the MM field of the new format (None disables that check).
    """
    if NEW_POST_RE.match(name):
        mm = int(name[3:5])
        if parent_month is not None and mm != parent_month:
            return False, (f"календарный месяц в имени MM={mm:02d} не совпадает "
                           f"с месяцем папки ({parent_month:02d})")
        return True, ""
    if LEGACY_POST_RE.match(name) or LEGACY_ALT_POST_RE.match(name):
        return True, ""
    if SERVICE_RE.match(name):
        return True, ""
    # Give the most useful hint we can about why it failed.
    if re.search(r"[А-Яа-яЁё]", name):
        return False, "русский slug — должен быть английский, через дефис"
    return False, ("не по шаблону {PP}-{MM}-{YYYY-MM-DD}-{slug} "
                   "(или legacy {NNN}-{YYYY-MM-DD}-{slug})")

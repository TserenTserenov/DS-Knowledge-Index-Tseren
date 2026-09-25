"""Python adapter for the shared knowledge-index publication convention.

The normative data lives in _publish_convention.json, read by this adapter
and the server scaffold. Both local creation and the naming guard import this
module; unavailable or invalid configuration has no hardcoded fallback.

Convention (see CLAUDE.md "3. Формат поста"):
  docs/{YYYY}/{NN}-{month}/{PP}-{MM}-{YYYY-MM-DD}-{slug}/
where NN = 13 - calendar_month (reverse: newest month sorts to the top on
GitHub), MM = real calendar month, PP = sequential post number within month.
"""

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from string import Formatter


class ConventionError(ValueError):
    """The shared convention cannot safely name a publication."""


TEMPLATE_FIELDS = {
    "month_dir": {"reverse_month", "month_name"},
    "post_dir": {"sequence", "month", "date", "slug"},
    "channel_file": {"sequence", "month", "channel_number", "channel", "date"},
}
PATTERN_GROUPS = {
    "slug": 0, "month_dir": 2, "new_post_prefix": 2, "new_post": 0,
    "legacy_post": 0, "legacy_alt_post": 0, "service": 0,
}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConventionError("Конвенция содержит повторяющееся поле.")
        result[key] = value
    return result


def _component(value: str) -> str:
    if (not isinstance(value, str) or not value or value in (".", "..")
            or len(value.encode("utf-8")) > 255
            or not re.fullmatch(r"[a-zа-яё0-9.-]+", value)):
        raise ConventionError("Конвенция создала недопустимый компонент пути.")
    return value


def _validate_template(name, template):
    if not isinstance(template, str) or not 1 <= len(template) <= 255:
        raise ConventionError(f"Некорректный шаблон конвенции: {name}.")
    if name == "channel_file" and not template.endswith(".md"):
        raise ConventionError("Шаблон файла канала должен оканчиваться на .md.")
    fields = []
    try:
        for literal, field, spec, conversion in Formatter().parse(template):
            if not re.fullmatch(r"[a-z0-9.-]*", literal) or spec or conversion:
                raise ConventionError(f"Недопустимый синтаксис шаблона: {name}.")
            if field is not None:
                fields.append(field)
    except ValueError as exc:
        raise ConventionError(f"Некорректный шаблон конвенции: {name}.") from exc
    if set(fields) != TEMPLATE_FIELDS[name] or len(fields) != len(TEMPLATE_FIELDS[name]):
        raise ConventionError(f"Недопустимые поля шаблона: {name}.")


def load_convention(path: Path):
    try:
        with path.open("rb") as source:
            raw = source.read(65_537)
        if len(raw) > 65_536:
            raise ConventionError("Файл конвенции превышает 64 КиБ.")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConventionError("Не удалось прочитать scripts/_publish_convention.json.") from exc
    expected = {"version", "reverse_month_base", "months_ru", "channels", "patterns",
                "non_month_dirs", "templates"}
    if not isinstance(data, dict) or set(data) != expected:
        raise ConventionError("Некорректные поля конвенции публикаций.")
    if type(data["version"]) is not int or data["version"] != 1:
        raise ConventionError("Неподдерживаемая версия конвенции публикаций.")
    if type(data["reverse_month_base"]) is not int or data["reverse_month_base"] != 13:
        raise ConventionError("Конвенция требует обратную нумерацию месяцев от 13.")
    months = data["months_ru"]
    if (not isinstance(months, list) or len(months) != 12
            or any(not isinstance(month, str) or not re.fullmatch(r"[а-яё]+", month) for month in months)
            or len(set(months)) != 12):
        raise ConventionError("В конвенции нужны 12 разных русских названий месяцев.")
    channels = data["channels"]
    if (not isinstance(channels, dict) or not channels or channels.get("club") != 1
            or any(not re.fullmatch(r"[a-z][a-z0-9]*", channel) for channel in channels)
            or any(type(number) is not int for number in channels.values())
            or set(channels.values()) != set(range(1, len(channels) + 1))):
        raise ConventionError("Некорректный реестр каналов конвенции.")
    patterns = data["patterns"]
    if not isinstance(patterns, dict) or set(patterns) != set(PATTERN_GROUPS):
        raise ConventionError("Некорректный набор правил имён конвенции.")
    for name, pattern in patterns.items():
        if not isinstance(pattern, str) or not 1 <= len(pattern) <= 512 or not pattern.startswith("^"):
            raise ConventionError(f"Некорректное правило имени: {name}.")
        if name != "new_post_prefix" and not pattern.endswith("$"):
            raise ConventionError(f"Правило имени должно охватывать всё имя: {name}.")
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            raise ConventionError(f"Некорректное регулярное выражение: {name}.") from exc
        if compiled.groups != PATTERN_GROUPS[name]:
            raise ConventionError(f"Некорректные группы правила имени: {name}.")
    skipped = data["non_month_dirs"]
    if (not isinstance(skipped, list) or not all(isinstance(item, str) for item in skipped)
            or len(set(skipped)) != len(skipped)):
        raise ConventionError("Некорректный список служебных каталогов.")
    for item in skipped:
        _component(item)
    templates = data["templates"]
    if not isinstance(templates, dict) or set(templates) != set(TEMPLATE_FIELDS):
        raise ConventionError("Некорректный набор шаблонов конвенции.")
    for name, template in templates.items():
        _validate_template(name, template)
    return data


CONVENTION = load_convention(Path(__file__).with_suffix(".json"))
CHANNELS = CONVENTION["channels"]
MONTHS_RU = dict(enumerate(CONVENTION["months_ru"], 1))
MONTH_BY_NAME = {name: num for num, name in MONTHS_RU.items()}
SLUG_RE = re.compile(CONVENTION["patterns"]["slug"])
MONTH_DIR_RE = re.compile(CONVENTION["patterns"]["month_dir"])
NEW_POST_PREFIX_RE = re.compile(CONVENTION["patterns"]["new_post_prefix"])
NEW_POST_RE = re.compile(CONVENTION["patterns"]["new_post"])
LEGACY_POST_RE = re.compile(CONVENTION["patterns"]["legacy_post"])
LEGACY_ALT_POST_RE = re.compile(CONVENTION["patterns"]["legacy_alt_post"])
SERVICE_RE = re.compile(CONVENTION["patterns"]["service"])
NON_MONTH_DIRS = set(CONVENTION["non_month_dirs"])


def reverse_month_number(month: int) -> int:
    """Reverse index so the newest month sorts first on GitHub (June -> 07)."""
    if type(month) is not int or not 1 <= month <= 12:
        raise ConventionError("Календарный месяц должен быть от 1 до 12.")
    return CONVENTION["reverse_month_base"] - month


def month_directory_name(month: int) -> str:
    reverse = reverse_month_number(month)
    name = _component(CONVENTION["templates"]["month_dir"].format(
        reverse_month=f"{reverse:02d}", month_name=MONTHS_RU[month]))
    match = MONTH_DIR_RE.fullmatch(name)
    if not match or int(match.group(1)) != reverse or match.group(2) != MONTHS_RU[month]:
        raise ConventionError("Шаблон месяца противоречит правилу его имени.")
    return name


@dataclass(frozen=True)
class PostNames:
    month_dir: str
    post_dir: str
    channel_files: dict[str, str]


def render_post_names(published_date: date, slug: str, sequence: int, channels) -> PostNames:
    if type(published_date) is not date:
        raise ConventionError("Нужна календарная дата публикации.")
    if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
        raise ConventionError("Некорректный slug публикации.")
    if type(sequence) is not int or not 1 <= sequence <= 99:
        raise ConventionError("Конвенция допускает месячный номер от 01 до 99.")
    selected = set(channels) | {"club"}
    if not selected.issubset(CHANNELS):
        raise ConventionError("Неизвестный канал публикации.")
    values = {"sequence": f"{sequence:02d}", "month": f"{published_date.month:02d}",
              "date": published_date.isoformat(), "slug": slug}
    post_dir = _component(CONVENTION["templates"]["post_dir"].format(**values))
    prefix = NEW_POST_PREFIX_RE.match(post_dir)
    if (not NEW_POST_RE.fullmatch(post_dir) or not prefix
            or prefix.group(1) != values["sequence"] or prefix.group(2) != values["month"]):
        raise ConventionError("Шаблон поста противоречит правилу его имени.")
    files = {}
    for channel in sorted(selected, key=lambda item: CHANNELS[item]):
        files[channel] = _component(CONVENTION["templates"]["channel_file"].format(
            **values, channel=channel, channel_number=str(CHANNELS[channel])))
    if len(set(files.values())) != len(files):
        raise ConventionError("Шаблон канала создаёт совпадающие имена файлов.")
    return PostNames(month_directory_name(published_date.month), post_dir, files)


def validate_month_dir(name: str):
    """Validate a "docs/{YYYY}/" child. Returns (ok: bool, reason: str)."""
    if name in NON_MONTH_DIRS:
        return True, ""
    m = MONTH_DIR_RE.fullmatch(name)
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
    if NEW_POST_RE.fullmatch(name):
        mm = int(name[3:5])
        if parent_month is not None and mm != parent_month:
            return False, (f"календарный месяц в имени MM={mm:02d} не совпадает "
                           f"с месяцем папки ({parent_month:02d})")
        return True, ""
    if LEGACY_POST_RE.fullmatch(name) or LEGACY_ALT_POST_RE.fullmatch(name):
        return True, ""
    if SERVICE_RE.fullmatch(name):
        return True, ""
    # Give the most useful hint we can about why it failed.
    if re.search(r"[А-Яа-яЁё]", name):
        return False, "русский slug — должен быть английский, через дефис"
    return False, ("не по шаблону {PP}-{MM}-{YYYY-MM-DD}-{slug} "
                   "(или legacy {NNN}-{YYYY-MM-DD}-{slug})")

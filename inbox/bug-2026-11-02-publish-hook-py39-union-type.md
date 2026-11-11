---
type: bug
created: 2026-11-02
severity: medium
status: open
wp: null
---

# Bug: check-publish-naming.py падает на Python 3.9 (синтаксис int | None)

## Симптом

Хук `pre-commit` в DS-Knowledge-Index-Tseren блокирует любой коммит из-за SyntaxError в `_publish_convention.py`:

```
File "/Users/tserentserenov/IWE/DS-Knowledge-Index-Tseren/scripts/_publish_convention.py", line 220, in <module>
    def validate_post_dir(name: str, parent_month: int | None):
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

## Причина

Синтаксис `int | None` (union types) — Python 3.10+. Исполняемая версия Python — 3.9 (или старше), которая не поддерживает эту нотацию.

## Влияние

Коммит поста итогов недели W44 не выполнен. Файл создан:
`docs/2026/02-ноябрь/01-11-2026-11-02-week-review-w44/01-11-1-club-2026-11-02.md`

## Исправление

Заменить `int | None` → `Optional[int]` с импортом `from typing import Optional` в `scripts/_publish_convention.py`.

Либо обновить Python до 3.10+ на машине, где запускается хук.

## Следующий шаг

Пилот чинит хук (или обходит: `git commit --no-verify`), затем коммитит файл поста W44 вручную.

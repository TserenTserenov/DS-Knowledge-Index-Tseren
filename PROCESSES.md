# PROCESSES.md — DS-Knowledge-Index-Tseren

> **Сценарий:** [DP.SC.005 Публикация контента](../PACK-digital-platform/pack/digital-platform/08-service-clauses/DP.SC.005-content-publishing.md)
> **Каталог сервисов:** [DP.MAP.002](../PACK-digital-platform/pack/digital-platform/07-map/DP.MAP.002-iwe-service-catalog.md)

---

## S46. Content Adaptation (Адаптация контента)

**Роль:** R4 Автор (Claude)
**Триггер:** Пользователь согласовал club-версию и запросил адаптации
**Вход:** `{NNN}-1-club-{date}.md` (status: draft, согласованный текст)
**Выход:** Файлы `{NNN}-{N}-{channel}-{date}.md` для каждого запрошенного канала

### Алгоритм

1. **Прочитать club-версию** (source-of-truth)
2. **Определить каналы** — спросить пользователя или взять из задания
3. **Для каждого канала** — создать файл по правилам канала:

| Канал | Что делать с club-версией |
|-------|--------------------------|
| `facebook` | Сохранить структуру и аргументацию. Укоротить абзацы. Убрать CTA на клуб. Добавить личный тон. Подзаголовки — по желанию |
| `linkedin` | Выбрать ОДИН ключевой инсайт. Первые 2 строки — крючок (видны до fold). Деловой тон. Убрать подзаголовки. Хэштеги 3-5 в конце |
| `telegram` | Крючок (1-2 предложения) + суть (3-5 предложений) + ссылка на клуб. Без markdown. 1-2 эмодзи |
| `tenchat` | Как LinkedIn, но длиннее. Подзаголовки допустимы. Хэштеги 5-10. Учитывать российскую бизнес-аудиторию |
| `x` | Провокационный заход. Одиночный твит (280 симв.) или тред (3-7). Каждый твит самодостаточен. Ссылка — в последнем |
| `youtube` | Только если есть видео. Структура: о чём (2-3 предложения) → таймкоды → ссылки |

4. **Frontmatter** каждого файла:
   - `target: {channel}`
   - `channel_number: {N}`
   - `source_post: "{NNN}-1-club-{date}.md"`
   - `status: draft`
5. **Показать пользователю** для согласования

### Правила адаптации

- **НЕ переписывать заново** — адаптировать, сохраняя авторский голос
- **НЕ добавлять новых аргументов** — только то, что есть в club-версии
- **НЕ ставить status: ready** — это делает пользователь после проверки
- **Каждый канал — отдельный файл** с полным frontmatter
- Если пользователь просит адаптацию только для некоторых каналов — создавать только запрошенные

---

## Публикация (существующие сервисы)

### S25. Daily Scan

> Реализация: бот (@aist_me_bot). Детали: [PROCESSES.md бота](../DS-IT-systems/aist_bot_newarchitecture/PROCESSES.md)

- Сканирует `docs/` рекурсивно (включая подпапки мультиканальных постов)
- Ищет файлы с `target: club` + `status: ready`
- Планирует публикацию в расписание

### S26. Scheduled Publish

- Публикует в Discourse по расписанию
- Обновляет `status: ready → published` через GitHub API

### S27. Manual Publish

- По команде `/club publish` — немедленная публикация

### S28. Comment Check

- Проверяет новые комментарии к опубликованным постам
- Уведомляет автора в TG

---

## S47. Multi-Channel Publish (Мультиканальная публикация)

**Роль:** R21 Публикатор
**Триггер:** `python social_publish.py publish <file>` или `python social_publish.py scan`
**Вход:** Файлы адаптаций с `status: ready` и `target: {channel}`
**Выход:** Пост опубликован в канале, `status → published`

### Поддерживаемые каналы

| Канал | API | Auth | Ограничения |
|-------|-----|------|-------------|
| `telegram` | Telegram Bot API | Bot token + channel admin | 4096 символов |
| `x` | X API v2 | OAuth 1.0a (4 ключа) | 280 символов (тред автоматически) |
| `linkedin` | Posts API | OAuth 2.0 (`w_member_social`) | 3000 символов |
| `facebook` | Graph API v25 | Page Access Token | ~63K символов |
| `tenchat` | — | — | ⚠ Ручной (нет API) |
| `youtube` | — | — | ⚠ Ручной (нет API community posts) |

### Алгоритм

1. Прочитать frontmatter: `target`, `status`
2. Если `status ≠ ready` → пропуск
3. Определить адаптер по `target`
4. Адаптер форматирует текст (markdown → формат канала)
5. Адаптер публикует через API канала
6. Обновить `status: ready → published` в файле

### CLI

```bash
# Опубликовать один файл:
python social_publish.py publish path/to/071-4-telegram-2026-03-18.md

# Сканировать и опубликовать все ready:
python social_publish.py scan [--dry-run]

# Показать статус файла:
python social_publish.py status path/to/file.md

# Показать доступные каналы:
python social_publish.py channels
```

### Конфигурация

Файл: `DS-IT-systems/DS-ai-systems/publisher/scripts/.env`
Шаблон: `.env.example`

### Реализация

Скрипт: [`DS-IT-systems/DS-ai-systems/publisher/scripts/social_publish.py`](../DS-IT-systems/DS-ai-systems/publisher/scripts/social_publish.py)

---

## S48. Cover Image Generation (Генерация обложки)

**Роль:** R4 Автор (Claude) или вручную
**Триггер:** Пост написан (club-версия согласована)
**Вход:** Файл поста `.md` с frontmatter
**Выход:** `cover.png` в директории поста

### Алгоритм

1. Прочитать пост → извлечь title, tags, первые 3 абзаца
2. Построить промпт: IWE-стиль (blueprint, navy + cyan + amber) + содержание поста
3. Вызвать DALL-E 3 API → получить PNG (1792x1024 — горизонтальная обложка)
4. Сохранить `cover.png` рядом с постом

### CLI

```bash
# Автоматический промпт из содержимого поста:
python generate_post_image.py path/to/post.md

# Кастомный промпт:
python generate_post_image.py path/to/post.md --prompt "три слоя экзокортекса"

# Квадратная (для соцсетей):
python generate_post_image.py path/to/post.md --size 1024x1024

# Dry-run (показать промпт без генерации):
python generate_post_image.py path/to/post.md --dry-run
```

### Конфигурация

API key: `~/IWE/.secrets/openai-api-key` или `OPENAI_API_KEY` env var
Стоимость: ~$0.04 (1024x1024) / ~$0.08 (1792x1024) за картинку

### Интеграция с публикаторами

Все публикаторы автоматически подхватывают `cover.png` при публикации:

| Публикатор | Как использует cover.png |
|------------|------------------------|
| S25/S26 (Discourse) | Upload через Discourse API → markdown `![](url)` в начало поста |
| S47 Telegram | `sendPhoto` с caption вместо `sendMessage` |
| S47 X | `media_upload` (v1.1) → `media_ids` в первый твит |
| S47 LinkedIn | Initialize upload → PUT binary → `content.media.id` в пост |
| S47 Facebook | `/{page_id}/photos` с `source` + `message` |

Если `cover.png` нет — публикация проходит как раньше (только текст).

### Реализация

Скрипт: [`DS-IT-systems/DS-ai-systems/publisher/scripts/generate_post_image.py`](../DS-IT-systems/DS-ai-systems/publisher/scripts/generate_post_image.py)

---

## Полный процесс: от идеи до всех каналов

```
Идея / заметка / черновик
       ↓
  [1] Автор + Claude: лонгрид для клуба (club)
       ↓
  [2] Пользователь: согласование club-версии
       ↓
  [2b] Claude (S48): генерация обложки (cover.png)
       ↓
  [3] Claude (S46): адаптации для запрошенных каналов
       ↓
  [4] Пользователь: согласование адаптаций
       ↓
  [5] Пользователь: status: ready на club-файле
       ↓
  ┌────┴──────────────────────────────────────┐
  [6] Бот (S25→S26):                         [7] Пользователь: status: ready
  автопубликация в клуб                       на адаптациях
  ↓                                           ↓
  [8] Бот (S28):                             [8] S47 (social_publish.py):
  уведомления о комментариях                  автопубликация в соцсети
                                              (TG, X, LinkedIn, Facebook)
```

> **Одноканальный режим:** шаги [1] → [2] → [5] → [6] → [8 клуб]. Без адаптаций.
> **Мультиканальный:** [1] → [2] → [3] → [4] → [5] → [6] → [7] → [8 соцсети].
> **TenChat / YouTube:** шаг [8] — ручная публикация (нет API).

---

*Последнее обновление: 2026-03-20*

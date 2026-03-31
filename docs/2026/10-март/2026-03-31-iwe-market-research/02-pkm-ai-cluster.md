# Кластер: PKM + AI

**Дата среза:** 31 марта 2026

Продукты управления личными знаниями с AI-слоем. Исторически — хранилища. Сейчас — попытки добавить агентность.

---

<details open>
<summary><b>Obsidian — локальный стандарт PKM</b></summary>

**URL:** https://obsidian.md | **Releases:** https://github.com/obsidianmd/obsidian-releases
**Финансирование:** bootstrapped. ~$2M ARR, 18 сотрудников, оценка ~$300-350M
**Сообщество:** 1.5M+ активных пользователей (фев 2026), r/ObsidianMD

### Архитектура

**Data layer:** flat Markdown files (.md) в локальной папке (vault). С августа 2025 — **Bases**: виртуальные database views поверх Markdown-файлов (фильтры, сортировка, формулы) без изменения формата хранения. JSON Canvas для визуальных карт.

**AI:** нет встроенного. Экосистема плагинов: Smart Connections, Text Generator, Copilot, Obsidian Copilot. Новинка март 2026: **obsidian-skills** — AI agents spec с нативной поддержкой Markdown + Bases + JSON Canvas.

**MCP-интеграция:** сторонний MCP-сервер через WebSocket (порт 22360) — прямой доступ Claude/ChatGPT к vault.

**Memory:** vault = persistent memory. Контекст между сессиями = файловая система.

**Интеграции:** Git (плагин), Calendar (плагин), Readwise. Нет нативных Linear/Slack.

**Бизнес-модель:** бесплатно (базовый) / Sync $4-8/мес / Publish $16/мес. Коммерческая лицензия убрана в 2025 (все бесплатны).

### Польза для knowledge worker

Абсолютный контроль над данными. Offline-first. 1000+ плагинов = почти любой workflow. Git-версионирование мышления. Самое большое community PKM-инструментов.

### Инфраструктура

Local-first + optional sync. Нет server-side processing. AI = только через внешние API (плагины). MCP как новый "plugin API" для AI-эры.

### Разрыв с IWE

Нет агентного слоя нативно. Нет ОРЗ-ритуалов. Нет Pack-архитектуры (иерархия source-of-truth). Нет рабочих продуктов с бюджетами. Нет мультипликатора. Это **хранилище**, IWE — **операционная система**.

**Ключевые ссылки:**
- https://obsidian.md/changelog/
- https://aitoolly.com/ai-news/article/2026-03-25-obsidian-skills-empowering-ai-agents-with-markdown-bases-and-json-canvas-integration
- https://forum.obsidian.md/t/i-built-an-mcp-server-that-connects-claude-ai-directly-to-your-obsidian-vault/112454

</details>

---

<details>
<summary><b>Notion AI / Notion 3.0 — workspace с агентами</b></summary>

**URL:** https://notion.com
**Финансирование:** оценка ~$10B (раунд 2021). 30M+ пользователей.
**Ключевой релиз:** Notion 3.0 (18 сент. 2025) — Agents. Notion 3.2 (янв. 2026) — мобильный AI, мультимодель.

### Архитектура

**Data layer:** проприетарная реляционная БД (cloud-only). Блочная структура. 20+ типов properties. Multi-source databases (нояб. 2025) — консолидация из разных workspace.

**AI:** нативный, глубоко встроен. Мультимодель (Notion 3.0+): GPT-5, Claude Opus 4.1, o3, Gemini 3. Авто-выбор модели по задаче.

**Агентный слой (Notion 3.0):** полноценный. Agents выполняют задачи до 20 минут автономно. Могут: создавать docs, строить databases, искать по workspace, исполнять multi-step workflows. Custom Agents: по расписанию или триггерам.

Для масштабирования агентов Notion **полностью снёс технический стек** (источник: VentureBeat): заменили task-specific prompt chains на центральную reasoning model + модульные sub-agents.

**Memory:** workspace = persistent memory. Agents используют Notion pages как state (page-as-memory).

**Интеграции:** Slack, Google Drive, MS Teams, Gmail (beta).

**Бизнес-модель:** Plus $10/user/мес, Business $15/user/мес (AI включён), Enterprise custom.

### Польза для knowledge worker

Самый зрелый workspace с агентами. Агент может делать то же что человек в Notion. AI Meeting Notes захватывает системный аудио. Мультимодельный выбор под задачу.

### Инфраструктура

Cloud-only (vendor lock-in). Export — lossy (теряется структура). Центральная reasoning model как orchestrator. Sub-agents для параллельного исполнения.

### Разрыв с IWE

Нет Pack-архитектуры (source-of-truth иерархии). Нет ОРЗ-фрактала (ритуалов открытия/закрытия). Нет мультипликатора. Нет git-native подхода. Коллаборативный = компромисс личного ownership. Проприетарный = зависимость от вендора.

**Ключевые ссылки:**
- https://www.notion.com/releases/2025-09-18 (Notion 3.0)
- https://venturebeat.com/ai/to-scale-agentic-ai-notion-tore-down-its-tech-stack-and-started-fresh
- https://www.notion.com/blog/introducing-notion-3-0

</details>

---

<details>
<summary><b>Tana — Knowledge Graph с daily rituals (ближайший аналог ОРЗ)</b></summary>

**URL:** https://tana.inc
**Финансирование:** $25M Series A (февр. 2025, Tola Capital + Lightspeed + Northzone). Оценка ~$100M. 160K+ waitlist. Fortune 500 — >80%.

### Архитектура

**Data layer:** Knowledge graph (cloud). Всё = nodes с bi-directional links. **Supertags** = схемы для типов данных (аналог классов в ООП): #task, #project, #person с кастомными полями. Offline-режим (добавлен 2025). Проприетарная graph БД.

**AI:** встроенный, мультипровайдер (OpenAI, Anthropic, Google). AI chat agents: поведение конфигурируется через Supertag-схему. Voice chat iOS: back-and-forth с AI через supertag-конфигурацию. AI-поля: авто-заполнение properties.

**Ритуалы (КЛЮЧЕВАЯ НАХОДКА):** Tana — **единственный продукт с Daily Page как structured ritual**. Daily Page с кнопками-workflow: morning pages, deep work prep, habit tracking, daily review с auto-generated journaling prompts. Это наиболее близкий аналог Day Open/Close в IWE. Настраивается через Supertags.

**Memory:** graph = persistent memory. Daily notes встроены в граф.

**Интеграции:** Meetings (нативный транскрибер), Calendar, Email импорт, API.

**Бизнес-модель:** SaaS, детали не раскрываются публично.

### Польза для knowledge worker

Типизированное знание = дисциплина мышления. Daily Page как ritual = структура дня. Voice-first capture. AI agents конфигурируются через структуру (не код). Офлайн.

### Инфраструктура

Cloud-first, graph-based. Supertag-схема = онтология домена (ближе всего к UL/BC из DDD). Мультипровайдерный AI.

### Разрыв с IWE

Нет ОРЗ-фрактала на трёх масштабах (сессия/день/неделя). Нет fallback chain (DS→Pack→Base). Нет рабочих продуктов с бюджетами. Нет мультипликатора. Нет git-native. Проприетарный граф = vendor lock-in.

**Ключевые ссылки:**
- https://techcrunch.com/2025/02/03/tana-snaps-up-25m-with-its-ai-powered-knowledge-graph-for-work-racking-up-a-160k-waitlist/
- https://outliner.tana.inc/articles/whats-new-in-tana-2025-product-updates
- https://outliner.tana.inc/articles/showcase-daily-notes

</details>

---

<details>
<summary><b>Capacities, Heptabase, Logseq, AFFiNE — специализированные PKM</b></summary>

### Capacities
**URL:** https://capacities.io | Bootstrapped, 100% user-funded

**Архитектура:** Object-based (Book, Meeting, Project — типизированные объекты с полями). Cloud sync. AI Chat поверх объекта, AI Property Auto-Fill. Провайдеры: OpenAI + Perplexity (добавлен 2025). Readwise интеграция.

**Польза:** объектное мышление — заметка как структурированный объект, не просто текст.

**Разрыв:** нет агентов, нет ритуалов, нет РП, нет мультипликатора.

---

### Heptabase
**URL:** https://heptabase.com | YC backed ($2.2M, 2022). Cash-flow positive. $1.2M ARR, рост 3x/год. 8 человек команда.

**Архитектура:** Local-first. Карточки + infinite whiteboard. Spatial organization (пространственное размещение). OpenAI/Claude через свой API ключ. Heptabase MCP (2025) — внешний доступ к vault. AI транскрипция аудио/видео.

**Польза:** visual thinking, spatial memory. Исследователи, creative professionals.

**Разрыв:** нет агентов, нет ОРЗ, нет РП, нет мультипликатора.

---

### Logseq
**URL:** https://logseq.com | GitHub: https://github.com/logseq/logseq (41,751 stars, AGPL-3.0)

**Архитектура:** **Переходный момент.** Classic mode = Markdown flat files (портативный). DB Version Beta = SQLite (производительность, структура). Форматы несовместимы. AI — только через плагины сообщества (нативный приостановлен во время рефакторинга). RTC (Real-Time Collaboration) в alpha.

**Польза:** outline-based thinking, bi-directional links, open-source — полный контроль.

**Разрыв:** нет AI нативно, нет агентов, нет ритуалов, нет РП.

**Ключевая ссылка:** https://github.com/logseq/logseq

---

### AFFiNE
**URL:** https://affine.pro | GitHub: https://github.com/toeverything/AFFiNE (40K+ stars, MIT/AGPL)

**Архитектура:** CRDT (y-octo на Rust + OctoBase). Два режима: Document + Edgeless (whiteboard). Self-hostable. Local-first + optional cloud. AI встроен (генерация, суммаризация).

**Польза:** open-source, CRDT = no conflicts, self-hostable = приватность.

**Разрыв:** нет агентного слоя, нет ритуалов, нет РП.

</details>

---

<details>
<summary><b>Mem.ai — AI-first PKM (rebuilt from scratch)</b></summary>

**URL:** https://get.mem.ai
**Финансирование:** $40M+ (OpenAI Startup Fund, оценка $110M)

### Архитектура

**Mem 2.0 (2025)** — полный rebuild. AI-first: нет папок, нет тегов. AI организует всё. Vector embeddings по всем заметкам. **Agentic Chat:** создаёт, редактирует, организует заметки автономно. Voice Mode. Deep Search. Контекст-resurfacing перед встречами.

**Memory:** Cloud vault + full offline (Mem 2.0). AI = механизм персистентности.

**Интеграции:** Google Calendar (bi-directional), Slack, Gmail.

### Польза

Нет overhead'а организации. AI делает классификацию. Контекст всплывает автоматически перед нужными встречами.

### Разрыв с IWE

Нет explicit иерархии знаний (Pack-архитектура). Нет ОРЗ-ритуалов. Нет РП. Нет мультипликатора. Cloud-only = нет контроля над данными.

**Ключевая ссылка:** https://get.mem.ai/blog/introducing-mem-2-0

</details>

---

<details>
<summary><b>Google NotebookLM — анализ источников на стероидах</b></summary>

**URL:** https://notebooklm.google
**Бизнес-модель:** бесплатно / NotebookLM Plus $19.99/мес / Enterprise custom. Gemini 3 upgrade — март 2026 (8x context window).

### Архитектура

Sources = загружаемые документы (до 300/notebook, до 500 notebooks). 1M token window Gemini 3. Audio Overviews (подкаст из документов, 80+ языков). Video Overviews, Infographics, Data Table (2025). NotebookLM Plus = out-of-box agent в Google Agentspace (enterprise).

### Польза

Deep Q&A по личному корпусу документов. Подкаст из PDF. Visual summaries. Образовательный контекст.

### Разрыв с IWE

Не PKM: это инструмент анализа источников, не постоянного знания. Нет cross-notebook memory. Нет агентов. Нет ритуалов. Нет РП. Пассивный ассистент, не ОС.

**Ключевые ссылки:**
- https://blog.google/technology/google-labs/notebooklm-custom-personas-engine-upgrade/

</details>

---

## Специальная таблица: IWE-концепции в PKM-продуктах

| Концепция | Tana | Obsidian | Notion 3.0 | Mem.ai | Logseq | IWE |
|-----------|------|----------|------------|--------|--------|-----|
| Ритуалы дня (Day Open/Close) | Да (Daily Page) | Через плагины | Через агентов | Нет | Daily journals | **Полноценный ОРЗ-фрактал** |
| Source-of-truth иерархия | Частично (Supertag schemas) | Нет | Нет | Нет | Нет | **DS→Pack→Base** |
| Рабочие продукты с бюджетом | Частично (#task с полями) | Нет | Через databases | Нет | Нет | **РП + бюджет + мультипликатор** |
| Мультипликатор | Нет | Нет | Нет | Нет | Нет | **2x+ физическое→интеллектуальное** |
| Git-native | Нет | Через плагин | Нет | Нет | Нет | **Да** |
| Self-hosted / local-first | Нет | **Да** | Нет | Нет | **Да** | **Да** |
| Агентные роли | Частично | Нет | Да | Частично | Нет | **Да (Портной, Оценщик...)** |

**Вывод:** Tana ближе всего к ОРЗ-концепции (Daily Page = прото-ritual), Obsidian — к data ownership. Ни один не совмещает все пять компонентов IWE.

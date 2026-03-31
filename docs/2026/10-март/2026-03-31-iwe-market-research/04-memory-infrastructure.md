# Кластер: Context Engineering & Memory Infrastructure

**Дата среза:** 31 марта 2026

Инфраструктурные системы для персистентной памяти AI-агентов. Это фундамент, на котором строится Personal AI OS.

---

## Почему memory — центральная проблема

Без персистентной памяти агент = stateless. Каждая сессия начинается с нуля. Для knowledge worker это означает: постоянный overhead на восстановление контекста, невозможность накопить "интеллектуальный капитал", нет обучения на опыте.

Три парадигмы решения (источник: [The State of Agent Memory 2026](https://blog.virenmohindra.me/p/the-state-of-agent-memory-2026), code review 10 репозиториев, $31.5M инвестиций):

| Парадигма | Кто | Принцип | Компромисс |
|-----------|-----|---------|------------|
| **System-Managed Extraction** | Mem0, Graphiti, Cognee | Инфраструктура решает что хранить | Дорогая запись, чистый вывод |
| **Agent Self-Management** | Letta (MemGPT) | Агент сам управляет через tools | Зависит от дисциплины агента |
| **Compression & Retrieval** | SimpleMem, mcp-memory-service | Сжатие истории, обмен точностью на токены | Потери при сжатии |

---

<details open>
<summary><b>Letta (ex-MemGPT) — агент как хозяин своей памяти</b></summary>

**GitHub:** https://github.com/letta-ai/letta (~21K stars)
**Cloud:** https://letta.com | **Arxiv (оригинал):** MemGPT, UCB 2023

### Польза

Агент знает о себе, о пользователе и о своей истории. Persona block = стабильная идентичность агента. Human block = накопленное знание о пользователе. Archival = неограниченное внешнее хранилище для долгосрочного контекста.

### Инфраструктура

**Трёхуровневая архитектура памяти (MemGPT-стиль):**

```
Core Memory (in-context, всегда):
  ├── persona block — кто я
  └── human block — кто пользователь

Recall Memory (поиск по истории разговоров)

Archival Memory (внешнее векторное хранилище, неограниченный объём)
```

Агент управляет перемещением данных между уровнями через **tool calls**: `memory_append`, `memory_replace`, `archival_memory_search`. Это ключевое: не инфраструктура решает, а сам агент.

**Letta V1 (2025, новая архитектура):** убирает `send_message` инструмент и heartbeats. Переход к нативному рассуждению моделей (GPT-5, Claude 4.5 Sonnet). Упрощение = меньше overhead на управление памятью.

**Multi-agent:** поддержка субагентов с общими состояниями. Self-hosted (open-source) + cloud.

### Разрыв с IWE

Инфраструктурный фреймворк (не end-user product). Нет PKM. Нет ритуалов. Нет Pack-архитектуры. Нет мультипликатора. IWE использует Letta-подобные концепции на уровне CLAUDE.md + memory/*.

**Ключевые ссылки:**
- https://www.letta.com/blog/letta-v1-agent
- https://github.com/letta-ai/letta

</details>

---

<details>
<summary><b>Mem0 — гибридная память, самый популярный OSS</b></summary>

**GitHub:** https://github.com/mem0ai/mem0 (~48K stars, Apache 2.0)
**Cloud:** https://mem0.ai | **Финансирование:** $24M

### Польза

+26% точности vs OpenAI Memory на LOCOMO benchmark. 91% быстрее full-context. 90% меньше токенов. Автоматическая экстракция без участия пользователя. Self-hosted до air-gapped enterprise.

### Инфраструктура

**Гибридная архитектура (три слоя):**
```
Vector DB — семантический поиск по фактам и предпочтениям
Key-Value DB — быстрый доступ по entity ID
Graph DB (Pro tier) — отношения между сущностями
```

При `add()` — LLM-пайплайн автоматически извлекает факты, сохраняет как атомарные записи. Extraction = полностью автоматическая.

**Multi-agent:** scoping по user/session/agent — у каждого агента своё пространство памяти.

**Self-hosted:** on-premises, private cloud, Kubernetes, air-gapped.

**Неожиданный инсайт** (code review Mohindra): Mem0 реализует mention-counting инфраструктуру для scoring по частоте упоминаний — но этот код **никогда не используется в retrieval**. Хорошая инфраструктура, оторванная от функциональности.

**Ключевые ссылки:**
- https://github.com/mem0ai/mem0
- https://blog.virenmohindra.me/p/the-state-of-agent-memory-2026

</details>

---

<details>
<summary><b>Zep + Graphiti — Temporal Knowledge Graph (лучший decay)</b></summary>

**GitHub:** https://github.com/getzep/graphiti (~20K stars)
**Arxiv:** [2501.13956](https://arxiv.org/abs/2501.13956) — Zep: A Temporal Knowledge Graph Architecture for Agent Memory

### Польза

**Единственная система** (вместе с Hindsight) с bi-temporal validity windows. Агент знает не только "что правда", но и "что было правдой в конкретный момент времени". LongMemEval: +18.5% точности. P95 latency: 300ms.

### Инфраструктура

**Трёхуровневый граф:**
```
Episode Subgraph — сырые входные данные (non-lossy)
Semantic Entity Subgraph — сущности и отношения (с разрешением дубликатов)
Community Subgraph — высокоуровневые тематические кластеры
```

**Би-темпоральная модель (ключевая инновация):**
- **Event Time (T)** — когда факт стал истинным в реальном мире
- **Ingestion Time (T')** — когда система узнала о факте

Каждый факт = validity window: когда стал истинным → когда вытеснен другим фактом. Можно запросить: "что мы знали о X в момент T?"

**Retrieval:** Interval tree indexing по временным диапазонам + семантический поиск. DMR benchmark: 94.8% vs 93.4% у MemGPT.

**Ключевые ссылки:**
- https://arxiv.org/abs/2501.13956
- https://github.com/getzep/graphiti
- https://blog.getzep.com/graphiti-hits-20k-stars-mcp-server-1-0/

</details>

---

<details>
<summary><b>LangMem — три типа памяти + background consolidation</b></summary>

**GitHub:** https://github.com/langchain-ai/langmem
**Docs:** https://langchain-ai.github.io/langmem/

### Инфраструктура

**Три типа памяти (по CoALA таксономии):**
```
Semantic Memory — факты и знания
  ├── Collections: неограниченный поиск по базе
  └── Profiles: единый schema-документ (обновляется в-месте)

Episodic Memory — успешные взаимодействия как примеры

Procedural Memory — поведенческие паттерны через system prompt
  (эволюционирует на основе feedback)
```

**Два режима формирования:**
- **"Conscious" (hot-path)** — немедленное обновление во время разговора (+latency)
- **"Subconscious" (background)** — анализ после разговора (0 влияния на скорость)

**Stateful Layer** — через LangGraph BaseStore с иерархическими namespaces. Нет decay (пробел).

**Ключевые ссылки:**
- https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
- https://blog.langchain.com/context-engineering-for-agents/

</details>

---

<details>
<summary><b>Khoj — Self-Hostable AI Second Brain</b></summary>

**GitHub:** https://github.com/khoj-ai/khoj (~10K stars) | **Cloud:** https://app.khoj.dev
**YC-backed**

### Польза

RAG по личным документам (PDF, Markdown, Notion, Org-mode). Собственный веб-поиск. Custom agents в контексте личных знаний. Scheduled automations. Deep Research mode. Obsidian + Emacs plugin.

### Инфраструктура

Semantic search по индексированным документам. Multi-LLM (любые модели). Self-hostable (Docker). Web search интегрирован нативно. Custom agents = RAG по личной базе + web.

### Разрыв с IWE

Нет ритуальных протоколов. Нет Pack-архитектуры. Нет мультипликатора. Нет рабочих продуктов. Khoj = intelligent search + RAG engine. IWE = full operational OS.

</details>

---

<details>
<summary><b>Claude Code Memory + COG second brain (независимая конвергенция)</b></summary>

### Claude Code Auto-Memory
**Docs:** https://docs.anthropic.com/en/docs/claude-code/memory

**Философия (Anthropic):** file-based, прозрачная память. Claude сам записывает: команды сборки, архитектурные решения, стиль кода. **AutoDream** = фоновая консолидация: pruning (устаревшее), merging (связанное), refreshing (реструктуризация).

Ставка на unification — Claude решает что извлекать, хранить и отвечать в едином conversational flow. Без отдельных векторных баз.

---

### COG second brain (huytieu)
**GitHub:** https://github.com/huytieu/COG-second-brain

**Концепция:** Cognition + Obsidian + Git. Только `.md` файлы + Claude Code Skills + Git. Без database, без vendor lock-in. 17 Claude Code skills, 7 role packs (Product Manager, Engineer, Designer, Founder...). 120+ braindumps processed, daily briefs с 95%+ source accuracy.

**Почему важно:** независимая конвергенция к архитектуре близкой к IWE. CLAUDE.md + memory files + git-versioned markdown. Несколько человек независимо пришли к похожим паттернам = подтверждение направления.

**Что отличает от IWE:** нет Pack/DS иерархии, нет ОРЗ-фрактала, нет мультипликатора. Это базовый слой без операционной методологии поверх него.

</details>

---

## Академические основания (arxiv)

### Ключевые работы по memory для агентов

| Работа | Ссылка | Суть |
|--------|--------|------|
| **MemOS (короткая)** | [arxiv 2505.22101](https://arxiv.org/abs/2505.22101) | MemCube abstraction: parametric + activation + plaintext unified |
| **MemOS (полная)** | [arxiv 2507.03724](https://arxiv.org/abs/2507.03724) | +159% temporal reasoning vs OpenAI. GitHub: [MemTensor/MemOS](https://github.com/MemTensor/MemOS) |
| **MemoryOS (EMNLP 2025 Oral)** | [arxiv 2506.06326](https://arxiv.org/pdf/2506.06326) | Иерархия short→mid→long. +48% F1 на LoCoMo. [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS) |
| **CoALA** | [arxiv 2309.02427](https://arxiv.org/abs/2309.02427) | Стандартная таксономия: working/episodic/semantic/procedural |
| **A-MEM (NeurIPS 2025)** | [arxiv 2502.12110](https://arxiv.org/abs/2502.12110) | Zettelkasten-метод для AI памяти. [agiresearch/A-mem](https://github.com/agiresearch/A-mem) |
| **Survey декабрь 2025** | [arxiv 2512.13564](https://arxiv.org/abs/2512.13564) | Factual/Experiential/Working. Пробелы: decay, multimodal, multi-agent concurrent writes |
| **Zep arxiv** | [arxiv 2501.13956](https://arxiv.org/abs/2501.13956) | Temporal KG: bi-temporal validity windows |

### Открытые проблемы (из survey 2512.13564)

1. **Decay/freshness** — только Zep и Hindsight решили. Большинство игнорируют.
2. **Parametric memory** — академически перспективно, в продуктах отсутствует
3. **Multi-agent concurrent writes** — нерешённая задача
4. **Memory automation** — экстракция всё ещё требует LLM-вызовов
5. **Trustworthiness** — как верифицировать что в памяти

---

## Сравнительная таблица memory систем

| Система | Stars | Тип памяти | Экстракция | Retrieval | Decay | Multi-agent | Self-hosted |
|---------|-------|------------|------------|-----------|-------|-------------|-------------|
| **Letta** | ~21K | 3 уровня (Core/Recall/Archival) | Агент сам | Агент-управляемый | Агент-контролируемый | Да | Да |
| **Mem0** | ~48K | Факты + граф (Pro) | Авто-LLM | Vector + Graph | Нет явного | Да (namespaces) | Да (air-gapped) |
| **Zep/Graphiti** | ~20K | Episodic/Semantic/Community | Авто entity | Bi-temporal + semantic | **Да (validity windows)** | Да | OSS + cloud |
| **LangMem** | — | Semantic/Episodic/Procedural | Авто (background) | Vector | Нет | Да | Да (LangGraph) |
| **Claude Code** | — | Markdown files | Авто (AutoDream) | Прямое чтение | AutoDream pruning | Нет | Нет |
| **Khoj** | ~10K | Document index | Индексация | Semantic | Нет | Нет | Да |
| **COG second brain** | — | Git-versioned markdown | Ручная | File-based | Git history | Нет | Да |

**Вывод:** IWE реализует file-based подход (как Claude Code), но с Pack-архитектурой как explicit source-of-truth иерархией — чего нет ни у кого из memory-инфраструктур.

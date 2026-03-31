# Позиционирование IWE: белые пятна, тренды, прогноз

**Дата среза:** 31 марта 2026

---

## Белые пятна рынка (что никто не делает)

### 1. Операционные ритуалы работы (главный белый кейс)

Все продукты предлагают инструменты. Никто не предлагает **методологию работы с инструментами**.

Tana — ближайший: Daily Page с morning routines. Но нет:
- Трёхмасштабной структуры (сессия / день / неделя)
- Протокола Закрытия с явной фиксацией результата
- Weekly review как обязательного элемента системы
- Верификации качества как отдельного шага (Haiku R23 в IWE)

**Потенциал:** первый, кто закроет этот пробел в mainstream PKM, получит категорию "work methodology OS".

---

### 2. Source-of-truth иерархия (Pack-архитектура)

Везде хранятся знания. Нигде нет явного ответа: **что является правдой при конфликте?**

- Notion: databases как правда, но нет fallback chain
- Tana: Supertag schema = правда о типе, но нет уровней
- Obsidian: нет стандартной иерархии

IWE решает: DS→Pack→Base. Если в DS противоречит Pack — Pack wins. Это OwnerIntegrity принцип. Нигде нет.

---

### 3. Мультипликатор времени

Ни один продукт не измеряет и не оптимизирует **отношение интеллектуального output к физическому времени**.

Все оптимизируют скорость отдельных задач. Никто не считает: "за X физических часов получен Y единиц интеллектуального output, коэффициент Z". WakaTime-подобный трекинг есть для кода, для knowledge work — нет.

---

### 4. Агентные роли с context isolation

Dust.tt = ближайший (builder/user разделение). Но нет:
- Формального ролевого протокола (кто активен в сессии?)
- Context isolation между ролями (Портной видит одно, Оценщик — другое)
- Переключения ролей как явного workflow-шага

---

### 5. Self-correction как первый класс

Везде AI может ошибаться. Нигде нет встроенного протокола:
- Замечено расхождение → немедленно предложить фикс (файл, строка, что изменить)
- Фиксация фиксов в memory для предотвращения повтора
- Self-correction как измеримая метрика качества системы

---

## Архитектурные тренды 2025-2026

### Тренд 1: MCP как новый "plugin API" для AI-эры

Obsidian, Heptabase, Guru, M365 Copilot, Zep — все добавили MCP. Anthropic (ноябрь 2024) + OpenAI AGENTS.md = Linux Foundation AAIF (декабрь 2025). MCP = стандарт. Через 1-2 года — базовое требование к любой системе. IWE использует нативно.

### Тренд 2: Local-first vs Cloud-first разлом

Obsidian/AFFiNE/Heptabase/COG second brain = local-first. Notion/Tana/Mem.ai = cloud-first. Logseq мигрирует к hybrid (SQLite + RTC). Meta купила Limitless (декабрь 2025) — wearable PKM не взлетел пока. CRDT (AFFiNE, Logseq DB version) = технологический ответ на offline-first sync. **IWE = git-as-truth, радикальный local-first.**

### Тренд 3: От workflow automation → к behavioral modeling

Lindy, ClickUp = автоматизация существующих workflow. Minro (YC S25) = репликация суждения пользователя через behavioral knowledge graph. Slashy = single-agent без MCP (anti-coordination). Движение: агент знает не что делать, а **как пользователь думает**. Minro — ближайшая точка к IWE по этой оси.

### Тренд 4: Temporal memory (bi-temporal validity)

Только Zep/Graphiti реализовали bi-temporal windows (event time + ingestion time). Survey декабрь 2025 идентифицирует это как нерешённую проблему. MemoryBank использовал Ebbinghaus decay академически. **Decay/freshness = открытая задача для всего рынка.**

### Тренд 5: Агенты как security principals

Microsoft Agent 365 (2026) — AI agents с identity/permissions/audit trail. Dust = 4-уровневый HITL. Glean = LLM judges. Governance AI = следующий уровень зрелости. IWE решает через Extension Gate + staging protocol — операционно, не через infrastructure security.

### Тренд 6: Wearable PKM — временно мертворождённый

Limitless/Rewind куплен Meta (декабрь 2025), продукт закрывается. Рынок не созрел. Но Meta куплено не зря — это инвестиция в будущее. Через 2-3 года wearable + persistent AI memory = следующий battleground.

---

## Прогноз: где окажется рынок к 2027-2028

### Сценарий 1: Notion/Tana wins "PKM OS"

Если Notion добавит structured sessions (ОРЗ-подобные) и Tana закроет L3-L4 — они могут занять позицию "Personal Work OS". Вероятность: средняя. Notion медленно добавляет personal features (исторически командный). Tana = ближе, но $25M = ограниченные ресурсы.

### Сценарий 2: Apple Notes + Siri = Mass Market Personal OS

Apple имеет миллиарды устройств, on-device модели, приватность. iOS 26: Markdown, Smart Categorization. Если добавят agent layer + cross-app memory = самый массовый Personal OS. Вероятность: высокая для mass market, но не для knowledge workers.

### Сценарий 3: Cursor/Claude Code wins "developer knowledge OS"

Karpathy: Claude Code = первый убедительный LLM-агент на личном компьютере. COG second brain, second-brain-skills = независимые реализации. Если Anthropic добавит PKM-возможности в Claude Code — это прямая конкуренция с IWE на developer сегменте.

### Сценарий 4: IWE-подобная методология становится категорией

Forte BASB AI pivot (февраль 2026) + Dreamer купленный Meta + Slashy "Cursor for knowledge workers" + YC S25 ~50% agentic = рынок движется к IWE-концепции. Первый продукт, который явно назовёт и реализует "Personal Work OS with rituals" — получает категорию.

---

## Позиционирование IWE

### Где уникален (абсолютно)

1. **ОРЗ-фрактал** — ритуальная методология на трёх масштабах
2. **Pack-архитектура** — explicit source-of-truth иерархия
3. **Мультипликатор** — измерение эффективности knowledge work
4. **WP Gate** — рабочий продукт как обязательный артефакт перед работой
5. **Priority Gate** — каждый РП связан с результатом R{N}

### Где конкуренция (частичное перекрытие)

| Конкурент | По какой оси |
|-----------|-------------|
| Tana | Daily rituals (L3 частично) |
| Notion 3.0 | Agent layer (L2) |
| Obsidian | PKM local-first (L1 + L5) |
| Dust.tt | Infrastructure-first philosophy |
| Letta | Memory architecture (L2 infrastructure) |
| COG second brain | Base architecture (CLAUDE.md + git) |
| Slashy | Narrative "Cursor for knowledge workers" |

### Целевой пользователь IWE vs конкурентов

| Тип пользователя | Лучший вариант |
|-----------------|----------------|
| Enterprise team knowledge | Dust.tt, Glean, M365 Copilot |
| Casual note-taker | Notion, Apple Notes |
| Developer productivity | Cursor, Claude Code + COG |
| Visual researcher | Heptabase |
| Advanced knowledge worker + methodology | **IWE** |
| Mass market personal AI | Tana (ближе всего) |

### Нарратив для клуба

**IWE — не ещё один инструмент для заметок.**

Рынок разделился: слева — хранилища знаний (Obsidian, Notion, Tana). Справа — агентные платформы (Dust, Glean, Microsoft). В центре — пустота: никто не ответил на вопрос **"как knowledge worker должен работать?"**

IWE отвечает именно на этот вопрос. Инструменты — вторичны. Первична методология:
- Каждое задание начинается с Открытия (что мы делаем, зачем)
- Каждый день имеет структуру (Day Open → Work → Day Close)
- Каждый рабочий продукт — явный артефакт с бюджетом и связью с результатом
- Знание накапливается иерархически (Pack = domain truth, DS = implementation)
- Физическое время множится на интеллектуальный output (мультипликатор ≥2x)

Академическое сообщество движется к этой концепции (MemOS, Science Exocortex). Бизнес — тоже (Dreamer куплен Meta, Slashy в YC). IWE = практически реализованная версия того, к чему рынок придёт через 2-3 года.

---

## Источники, верифицированные в ходе исследования

**Продукты:**
- https://obsidian.md/changelog/
- https://www.notion.com/releases/2025-09-18
- https://tana.inc/articles/whats-new-in-tana-2025-product-updates
- https://get.mem.ai/blog/introducing-mem-2-0
- https://dust.tt/blog/mcp-and-enterprise-agents-building-the-ai-operating-system-for-work
- https://www.glean.com/blog/emerging-agent-stack-2026
- https://news.ycombinator.com/item?id=45129031 (Slashy architecture)
- https://community.fibery.io/t/fibery-strategy-2026/10170

**Memory infrastructure:**
- https://github.com/letta-ai/letta
- https://github.com/mem0ai/mem0
- https://github.com/getzep/graphiti
- https://blog.getzep.com/graphiti-hits-20k-stars-mcp-server-1-0/
- https://langchain-ai.github.io/langmem/
- https://blog.virenmohindra.me/p/the-state-of-agent-memory-2026

**Академические:**
- https://arxiv.org/abs/2505.22101 (MemOS short)
- https://arxiv.org/abs/2507.03724 (MemOS full)
- https://arxiv.org/pdf/2506.06326 (MemoryOS EMNLP 2025)
- https://arxiv.org/abs/2309.02427 (CoALA)
- https://arxiv.org/abs/2502.12110 (A-MEM NeurIPS 2025)
- https://arxiv.org/abs/2512.13564 (Survey декабрь 2025)
- https://arxiv.org/abs/2501.13956 (Zep temporal KG)
- https://pubs.rsc.org/en/content/articlelanding/2024/dd/d4dd00178h (Science Exocortex RSC)
- https://generativeaiandhci.github.io/papers/2025/genaichi2025_51.pdf (Brain Cache CHI 2025)

**Исторические:**
- https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/ (Bush 1945)
- https://www.dougengelbart.org/pubs/papers/scanned/Doug_Engelbart-AugmentingHumanIntellect.pdf (Engelbart 1962)
- https://numinous.productions/ttft/ (Matuschak+Nielsen 2019)
- https://augmentingcognition.com/ (Nielsen 2018)
- https://benhouston3d.com/blog/origins-of-the-term-exocortex (термин exocortex)

**Community & авторы:**
- https://lilianweng.github.io/posts/2023-06-23-agent/ (Weng)
- https://simonwillison.net/2025/Dec/31/the-year-in-llms/ (Willison)
- https://maggieappleton.com/home-cooked-software (Appleton)
- https://karpathy.bearblog.dev/year-in-review-2025/ (Karpathy)
- https://fortelabs.com/blog/introducing-the-ai-second-brain/ (Forte)
- https://www.latent.space/p/dreamer (Dreamer → Meta)

**Отраслевые:**
- https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/ (AAIF)
- https://9to5mac.com/2025/12/05/rewind-limitless-meta-acquisition/ (Limitless → Meta)
- https://venturebeat.com/ai/to-scale-agentic-ai-notion-tore-down-its-tech-stack-and-started-fresh
- https://temporal.io/blog/how-dust-builds-agentic-ai-temporal
- https://www.cbinsights.com/research/y-combinator-spring25-agentic-ai/ (YC S25 analysis)

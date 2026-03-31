# Академические основания и исторический контекст

**Дата среза:** 31 марта 2026

---

## Исторические корни: от Memex до IWE

### Vannevar Bush — «As We May Think» (1945)

**Источник:** The Atlantic, июль 1945 — https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/

Первая формализованная концепция персонального устройства расширения памяти. **Memex** = механическая система ассоциативного хранения: книги, записи, коммуникации. Ключевая идея: не иерархическая классификация (как библиотека), а **ассоциативные trails** — персональные цепочки связей, сохраняемые и передаваемые.

Прямой предшественник PKM, графов знаний и personal AI OS. Написано за 46 лет до WWW, за 78 лет до MemGPT.

---

### Douglas Engelbart — «Augmenting Human Intellect» (1962)

**Источник:** Stanford Research Institute, октябрь 1962 — https://www.dougengelbart.org/pubs/papers/scanned/Doug_Engelbart-AugmentingHumanIntellect.pdf

Концепция **Intelligence Augmentation (IA)** как альтернатива "Artificial Intelligence". Синергия человека и машины — не замещение. Ввёл термин **H-LAM/T** (Human using Language, Artifacts, Methodology, in which he is Trained).

Engelbart изобрёл мышь, hypertext, videoconferencing — всё ради IA, не AI. Его framework объясняет IWE: среда, которая augments, а не automates мышление.

---

### Термин «exocortex» — Ben Houston (1998-1999)

**Источник:** https://benhouston3d.com/blog/origins-of-the-term-exocortex

Студент-когнитивист Бен Хьюстон ввёл термин по аналогии с неокортексом ("новой корой") для обозначения органа вне мозга, поддерживающего высокоуровневое мышление. Развитие идей Licklider и Engelbart о плотно связанных интерфейсах мозг-компьютер. IWE = современная реализация концепции экзокортекса с AI-слоем.

---

### Andy Matuschak & Michael Nielsen — «Tools for Thought» (2019)

**Источник:** https://numinous.productions/ttft/

Манифест: почему tools for thought (от Memex до Anki) системно **недоинвестированы**. Как создать среду, в которой мышление становится радикально мощнее. Ключевой тезис: трансформативные инструменты требуют новых медиа — не просто автоматизации существующих практик.

**Michael Nielsen — «Augmenting Long-term Memory»** (2018): https://augmentingcognition.com/ — память как активный инструмент мышления, не пассивное хранилище.

---

## Ключевые академические работы (2023-2026)

### CoALA: Cognitive Architectures for Language Agents

**Arxiv:** [2309.02427](https://arxiv.org/abs/2309.02427) | Авторы: Sumers, Yao, Narasimhan, Griffiths (Princeton) | Сент. 2023, v3 март 2024

Стала **стандартной таксономией** для архитекторов агентных систем. Три измерения:

```
Information Storage:
  ├── Working Memory (in-context, текущая задача)
  └── Long-term Memory:
      ├── Episodic (прошлые взаимодействия)
      ├── Semantic (факты и знания)
      └── Procedural (навыки и паттерны)

Action Space:
  ├── Internal (memory R/W, reasoning)
  └── External (environment, tools)

Decision-Making:
  ├── Planning
  └── Execution loop
```

Все последующие работы по memory агентов ссылаются на CoALA.

---

### MemOS: An Operating System for Memory-Augmented Generation

**Arxiv (short):** [2505.22101](https://arxiv.org/abs/2505.22101), май 2025, 22 соавтора
**Arxiv (full):** [2507.03724](https://arxiv.org/abs/2507.03724), июль 2025, v4 декабрь 2025, 39 соавторов
**GitHub:** https://github.com/MemTensor/MemOS
**Media:** [VentureBeat](https://venturebeat.com/ai/chinese-researchers-unveil-memos-the-first-memory-operating-system-that-gives-ai-human-like-recall/)

Первая работа, поднимающая память до уровня **first-class operational resource** с lifecycle management.

**Ключевая абстракция — MemCube:**
```
MemCube = контейнер памяти:
  ├── Content (сам факт/знание)
  └── Metadata (provenance, versioning, timestamps)

Три типа памяти в одной системе:
  ├── Parametric Memory (знание в весах модели)
  ├── Activation Memory (runtime context, KV-cache)
  └── Plaintext Memory (внешние хранилища)

Lifecycle: MemReader → MemScheduler → MemLifecycle → MemOperator
Операции: generation, activation, fusion, archiving, expiration
```

**Результат:** +159% boost в temporal reasoning vs OpenAI memory systems.

**Почему важно для IWE:** академическое подтверждение OS-метафоры для AI memory. IWE = практическая реализация MemOS-концепции на уровне knowledge worker, а не LLM-инфраструктуры.

---

### MemoryOS: Memory OS for AI Agents (EMNLP 2025 Oral)

**Arxiv:** [2506.06326](https://arxiv.org/pdf/2506.06326) | ACL Anthology: [2025.emnlp-main.1318](https://aclanthology.org/2025.emnlp-main.1318/)
**GitHub:** https://github.com/BAI-LAB/MemoryOS | Авторы: Jiazheng Kang et al. (BAI-LAB)

Иерархическая система хранения (вдохновлена OS memory management):
```
Short-term Memory → Mid-term Memory → Long-term Personal Memory
  (FIFO)              (segmented pages)   (consolidated knowledge)
```

**Benchmark LoCoMo:** +48.36% F1, +46.18% BLEU-1 vs GPT-4o-mini baseline. EMNLP Oral = высокая оценка peer reviewers.

---

### Memory in the Age of AI Agents: A Survey (декабрь 2025)

**Arxiv:** [2512.13564](https://arxiv.org/abs/2512.13564) | GitHub: [Shichun-Liu/Agent-Memory-Paper-List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)

Самый полный survey. Таксономия по функциям: Factual / Experiential / Working. По форме: Token-level / Parametric / Latent. Lifecycle: Formation → Evolution → Retrieval.

**Открытые проблемы:** memory automation (без LLM-overhead), RL integration, multimodal memory, multi-agent coordination, trustworthiness.

---

### A-MEM: Agentic Memory for LLM Agents (NeurIPS 2025)

**Arxiv:** [2502.12110](https://arxiv.org/abs/2502.12110) | GitHub: https://github.com/agiresearch/A-mem

Zettelkasten-метод для AI памяти. При добавлении новой памяти: генерация note с атрибутами (описание, keywords, tags) + динамическое связывание с существующими узлами. Selective top-k retrieval с эволюцией сети. Воспроизводит ручную методологию Luhmann автоматически.

---

### Towards a Science Exocortex (RSC, 2024)

**Журнал:** Digital Discovery (Royal Society of Chemistry)
**DOI:** [10.1039/D4DD00178H](https://pubs.rsc.org/en/content/articlelanding/2024/dd/d4dd00178h) | **Arxiv:** [2406.17809](https://arxiv.org/abs/2406.17809)
**Автор:** Kevin G. Yager (Brookhaven National Laboratory)

Первая детальная академическая архитектура экзокортекса для научного исследования. **Рой AI-агентов**, каждый из которых автоматизирует конкретные задачи учёного. Межагентная коммуникация порождает emergent behavior, расширяющий когнитивные способности.

Концептуально близко к IWE: несколько специализированных агентов (роли) + общий контекст (Pack) + emergence от взаимодействия.

---

### Brain Cache: Cognitive Exoskeleton (CHI 2025)

**Источник:** [generativeaiandhci.github.io/papers/2025/genaichi2025_51.pdf](https://generativeaiandhci.github.io/papers/2025/genaichi2025_51.pdf)

GenAI как когнитивный экзоскелет для экстернализации и структурирования знаний. Первое использование термина "cognitive exoskeleton" в академическом HCI-контексте. Подтверждает: рынок идёт к этой концепции через академию.

---

## Ключевые авторы и их позиции (март 2026)

### Andrej Karpathy — Software 3.0 / LLM OS

**Блог:** https://karpathy.bearblog.dev/year-in-review-2025/
**YC AI Startup School 2025:** "Software Is Changing (Again)"

Три эпохи ПО: классический код (1.0) → нейросети (2.0) → **LLM как новый вид компьютера (3.0)**. LLM одновременно является утилитой, фабом и операционной системой. Личный workflow: Cursor для tab-completion (~75% AI-использования), **Claude Code как первый убедительный пример LLM-агента на личном компьютере**.

Разбор на Latent Space: https://www.latent.space/p/s3

---

### Lilian Weng — Таксономия памяти агентов

**Ключевая статья:** [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) (июнь 2023)

Базовый справочник: Agent = LLM + memory + planning + tools. Типология памяти: sensory / short-term (in-context) / long-term (vector store). До сих пор стандарт для архитекторов. **Cited by CoALA, MemOS, все survey работы**.

---

### Simon Willison — Практик персональной AI-инфраструктуры

**Блог:** https://simonwillison.net
**2025 Year in LLMs:** https://simonwillison.net/2025/Dec/31/the-year-in-llms/

"Deep Research pattern works really well; coding agents are a much bigger deal than I expected." LLM CLI tool (Python) — персональная инфраструктура работы с моделями. Позиция: frontier-модели для daily drivers, локальные — ещё не готовы для агентных задач. Критичен к OpenAI Memory: [I really don't like ChatGPT's new memory dossier](https://simonwillison.net/2025/May/21/chatgpt-new-memory/).

---

### Maggie Appleton — Home-Cooked Software (май 2024)

**Эссе:** https://maggieappleton.com/home-cooked-software

LLM-ы открывают эпоху **«домашнего ПО»** для **«barefoot developers»** — людей с базовыми навыками, строящих инструменты для своих сообществ. Агенты должны стать оркестраторами, помогающими писать спецификации и подключать инфраструктуру. Январь 2026: работает в GitHub Next над инструментами на базе AI-агентов.

---

### Tiago Forte — BASB AI Pivot (февраль 2026)

**BASB:** https://www.buildingasecondbrain.com
**AI pivot:** https://fortelabs.com/blog/introducing-the-ai-second-brain/

400 000 экземпляров книги. В феврале 2026 — официальный AI-first pivot BASB. Следующая книга "Life in Perspective" (нояб. 2026) — система ежегодного ревью. PARA-метод (Projects/Areas/Resources/Archives) + AI = структурированная внешняя память. Forte всё больше видит AI-агентов как **активных участников системы**, не просто инструменты поиска.

**Структурное сходство с IWE:** CODE (Capture→Organize→Distill→Express) ≈ ОРЗ-фрактал. PARA ≈ Pack/DS разделение. IWE = BASB следующего поколения с операционным AI-слоем.

---

## Отраслевые стандарты (2025-2026)

### AAIF — Agentic AI Foundation (декабрь 2025)

**Источник:** [TechCrunch](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/)

OpenAI + Anthropic + Block основали AAIF под Linux Foundation.
- Anthropic донировал **MCP** (Model Context Protocol)
- OpenAI донировал **AGENTS.md**

Цель — открытая стандартизация агентной инфраструктуры, аналог TCP/IP для агентов. IWE использует MCP нативно (CLAUDE.md → MCP-серверы). Это подтверждение правильности архитектурного выбора.

---

### Dreamer → Meta Superintelligence Labs (март 2026)

**Latent Space:** https://www.latent.space/p/dreamer

Dreamer (David Singleton, ex-Stripe CTO + Hugo Barra) = **Personal Agent OS** с архитектурой ОС:
```
dreamer.com = GUI
Agents = user space
Sidekick (агент строящий агентов) = ядро ОС
Tools = драйверы устройств
```

Приобретён Meta Superintelligence Labs, март 2026. **Сигнал:** Meta видит Personal Agent OS как стратегическое направление. Dreamer = consumer-first реализация концепции, аналогичной IWE, купленная за высокую цену.

---

### OpenDAN — Personal AI OS (open-source)

**GitHub:** https://github.com/fiatrete/OpenDAN-Personal-AI-OS (2023-2024)

Первый open-source проект с явным именованием «Personal AI OS». AI BUS как шина, агенты с собственной памятью, AI Workflows. Docker-деплой на PC/Mac/RPi/NAS. Акцент на приватность: единый интерфейс контроля доступа к личным данным. Менее активен чем Khoj/Letta, но концептуально пионерский.

---

## Хронология ключевых идей

```
1945 — Bush: Memex, ассоциативные trails
1962 — Engelbart: Intelligence Augmentation, H-LAM/T
1998 — Houston: термин "exocortex"
2018 — Nielsen: Augmenting Long-term Memory
2019 — Matuschak+Nielsen: Tools for Thought манифест
2023 — CoALA: стандартная таксономия agent memory
2023 — MemGPT/Letta: OS-метафора для LLM memory
2024 — Yager: Science Exocortex (RSC)
2024 — Appleton: Home-Cooked Software & Barefoot Developers
2025 — MemOS: MemCube, unified memory OS (SJTU)
2025 — MemoryOS: hierarchical memory (EMNLP Oral)
2025 — A-MEM: Zettelkasten для AI (NeurIPS)
2025 — Survey: открытые проблемы memory
2025 — AAIF: стандартизация MCP + AGENTS.md
2025 — Forte: BASB AI pivot
2026 — Dreamer → Meta: Personal Agent OS куплен
2026 — Karpathy: Software 3.0, LLM как ОС
```

**Позиция IWE в этой хронологии:** практическая реализация идей из всех слоёв — от Engelbart (augmentation) до MemOS (unified memory) до CoALA (agent architecture), с уникальным добавлением: **операционная методология работы** (ОРЗ-фрактал, Pack-иерархия, мультипликатор).

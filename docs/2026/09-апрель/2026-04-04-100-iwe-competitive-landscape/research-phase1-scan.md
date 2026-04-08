# Scout Phase 1: Конкурентная разведка IWE

> Дата сбора: 2026-04-03
> Фаза: 1 (быстрый сбор, без глубокого анализа)
> Источники: GitHub Topics (exocortex, second-brain, ai-operating-system), WebSearch x18, HackerNews, Product Hunt, YC S25/W25

---

## Категория 1 — Прямые аналоги (экзокортексы / personal knowledge OS)

> Системы, совмещающие: персональная база знаний + AI-агент + методология работы

| Название | URL | Описание (1 предложение) | Категория | Размер |
|----------|-----|--------------------------|-----------|--------|
| **Khoj** | https://github.com/khoj-ai/khoj | Self-hostable AI second brain: ответы из docs/веба, агенты, автоматизации, поддержка любого LLM | 1 | 33.8k звезд |
| **Reor** | https://github.com/reorproject/reor | Приватное локальное AI-приложение для заметок: автолинковка, семантический поиск, RAG — всё через Ollama | 1 | 8.5k звезд |
| **Ars Contexta** | https://github.com/agenticnotetaking/arscontexta | Claude Code плагин, генерирующий персонализированную knowledge-систему через разговор (3-пространственная архитектура, 26 команд) | 1 | 2.9k звезд |
| **OpenDAN Personal AI OS** | https://github.com/fiatrete/OpenDAN-Personal-AI-OS | Открытая Personal AI OS, объединяющая AI-модули для создания личных агентов с управлением IoT и privacy | 1 | 2k звезды |
| **Neurite** | https://github.com/satellitecomponent/Neurite | Фрактальный граф-мышления: mind-mapping для AI-агентов, веб-ссылок, заметок и кода | 1 | 2k звезды |
| **Daniel Miessler PAI** | https://github.com/danielmiessler/Personal_AI_Infrastructure | Агентная AI-инфраструктура для усиления человека: TELOS-файлы, 6-уровневая кастомизация, skill-роутинг, постоянная память | 1 | 11k звезд |
| **wikibonsai** | https://github.com/wikibonsai/wikibonsai | Структурированный слой знаний в plain-text с семантическим граф-слоем | 1 | 96 звезд |
| **exocortex-halo** | https://github.com/virtadpt/exocortex-halo | Набор Python-ботов для расширения Huginn: поиск, архивирование, уведомления, контроль медиа | 1 | 76 звезд |
| **fuwasegu/exocortex** | https://github.com/fuwasegu/exocortex | Централизованный экзокортекс с семантическим поиском паттернов из истории разработки, всё локально | 1 | <20 звезд |
| **wbic16/exocortex** | https://github.com/wbic16/exocortex | "Экзокортекс 2130 версия 1.0" — философский проект когнитивной инфраструктуры | 1 | 4 звезды |
| **forkwright/aletheia** | https://github.com/forkwright/aletheia | Distributed cognition system: инфраструктура, инструментарий и непрерывность познания | 1 | 1 звезда |
| **TomDream/exocortex** | https://github.com/TomDream-app/exocortex | Внешнее пространство мышления для эмерджентных когнитивных структур и визуального экзокортекса | 1 | 0 звезд |
| **Second Brain (raold)** | https://github.com/raold/second-brain | 100% локальный second brain: документы, изображения, LLM (LLaVA/CLIP), граф знаний, без облака | 1 | <50 звезд |
| **Second Brain (henrydaum)** | https://github.com/henrydaum/second-brain | Десктоп-приложение: RAG, мультимодальные AI-модели, гибридный лексико-семантический поиск по локальным файлам | 1 | <100 звезд |
| **Second Brain Agent (flepied)** | https://github.com/flepied/second-brain-agent | AI second brain агент на LangChain для работы с личной базой знаний | 1 | <50 звезд |
| **obsidian-claude-pkm** | https://github.com/ballred/obsidian-claude-pkm | Полный стартовый кит: Obsidian + Claude Code для персонального PKM | 1 | 1.3k звезд |
| **Screenpipe** | https://github.com/screenpipe/screenpipe | AI-память экрана: непрерывная локальная запись активности, агенты на фоне, open-source Rewind | 1 | 18k звезд |
| **Second Me (me.bot)** | https://www.producthunt.com/products/mindos | Платформа для создания AI-копии себя с self-hosted хранением данных | 1 | Product Hunt |
| **Limitless (ex-Rewind)** | https://limitless.ai | Носимый + software AI для памяти разговоров (куплен Meta 2025) | 1 | Коммерческий |
| **Mem.ai** | https://mem.ai | AI-first workspace: автоорганизация заметок, семантический поиск, генерация из знаний | 1 | Коммерческий |
| **Reflect Notes** | https://reflect.app | Сетевые заметки + AI + календарь, iOS/macOS-ориентирован | 1 | Коммерческий |
| **Tana** | https://tana.inc | PKM с supertags и AI: граф-база, structured data как семантика, power users | 1 | Коммерческий |
| **Capacities** | https://capacities.io | Object-based PKM "studio for your mind" с AI-чатом поверх объектов знаний | 1 | Коммерческий |
| **Notion AI** | https://notion.so | Workspace + AI-генерация/суммаризация/поиск поверх базы знаний команды | 1 | 100M+ users |

---

## Категория 2 — AI-обёртки и оркестраторы поверх LLM

> Инструменты для построения персонального помощника поверх чужих моделей

| Название | URL | Описание (1 предложение) | Категория | Размер |
|----------|-----|--------------------------|-----------|--------|
| **Fabric (danielmiessler)** | https://github.com/danielmiessler/Fabric | Open-source фреймворк усиления человека через AI: 200+ паттернов-промптов, CLI, 40+ провайдеров | 2 | 40.4k звезд |
| **AnythingLLM** | https://github.com/Mintplex-Labs/anything-llm | All-in-one AI: чат с документами, агенты, RAG, мультипользователь, 30+ LLM провайдеров | 2 | 57.5k звезд |
| **Goose (Block)** | https://github.com/block/goose | Расширяемый open-source AI-агент: install/execute/edit/test с любым LLM, локально | 2 | 31k звезд |
| **Open WebUI** | https://github.com/open-webui/open-webui | Self-hosted UI для Ollama и OpenAI-совместимых API с агентами, базой знаний, голосом | 2 | 100k+ звезд |
| **LobeHub / LobeChat** | https://github.com/lobehub/lobe-chat | Extensible UI для multi-LLM с агент-маркетплейсом, knowledge base, PWA | 2 | 60k+ звезд |
| **LibreChat** | https://github.com/danny-avila/LibreChat | Enhanced ChatGPT-клон: все AI-провайдеры, агенты, MCP, multi-user, self-hosted | 2 | 30k+ звезд |
| **CoPaw** | https://github.com/agentscope-ai/CoPaw | Персональный AI-ассистент с полностью локальным деплоем без API-ключей | 2 | <1k звезд |
| **Mem0** | https://github.com/mem0ai/mem0 | Универсальный memory layer для AI-агентов: вектор + граф + KV хранилище, любой LLM | 2 | 37k звезд |
| **ARI** | https://github.com/Ari-OS/ARI | Personal AI OS с 7-уровневой архитектурой, тройной когницией (LOGOS/ETHOS/PATHOS), SHA-256 аудитом | 2 | 5 звезд |
| **Second Brain Starter (coleam00)** | https://github.com/coleam00/second-brain-starter | Claude Code скилл: генерирует персонализированный PRD для проактивного AI second brain | 2 | <100 звезд |
| **embraOS** | https://github.com/Ward-Software-Defined-Systems/embraOS | Continuity-preserving AI OS с памятью, эволюционирующий через время (Rust) | 2 | 1 звезда |
| **Aetherra** | https://github.com/AetherraLabs/Aetherra | Самоэволюционирующий AI-нативный язык и платформа для интеллектуальных агентов | 2 | 7 звезд |
| **Personal AI (personal.ai)** | https://personal.ai | Персональный AI-ассистент с собственной моделью, обученной на личных данных пользователя | 2 | Коммерческий |
| **Lindy AI** | https://lindy.ai | AI-ассистент: email, встречи, CRM, автоматизации — проактивный персональный агент | 2 | Коммерческий |

---

## Категория 3 — Structured AI workflows / культура работы с AI

> Системы, формализующие протоколы взаимодействия с AI: чеклисты, gates, протоколы

| Название | URL | Описание (1 предложение) | Категория | Размер |
|----------|-----|--------------------------|-----------|--------|
| **ZK Context Vault** | https://github.com/SyntaxAsSpiral/zk-context-vault | Комплексная когнитивная инфраструктура: 7 слоёв (Principles/Skills/Agents/Prompts/Artifacts/Workshop/Exocortex), slice-архитектура | 3 | 2 звезды |
| **Strategy-OS** | https://github.com/BellaBe/strategy-os | Автономная validation-система для соло-фаундеров: 3 агента, Hypothesis Register, Gap Register | 3 | 23 звезды |
| **Cognitive Prompt Architecture** | https://github.com/entrepeneur4lyf/cognitive-prompt-architecture | Инструментарий для принятия решений через структурированные когнитивные подходы к LLM | 3 | <50 звезд |
| **Prompt Decorators** | https://github.com/smkalami/prompt-decorators | Структурированные префиксы-декораторы для AI-ответов (аналог Python-декораторов) | 3 | <100 звезд |
| **Daniel Rosehill Agent Workspace** | https://github.com/danielrosehill/AI-Agent-Workspace-Spec-310325 | Спецификация персонального AI agent workspace: 1000+ system prompts, Agent Studio, Frontend | 3 | <50 звезд |
| **LC-OS-Project** | https://github.com/LivingFramework/LC-OS-Project | Practitioner toolkit с шаблонами и гайдами для AI workflow adoption | 3 | 4 звезды |
| **t9os** | https://github.com/HanbeenMoon/t9os | Философская OS для AI-человеческой индивидуации, построена на Claude Code | 3 | 2 звезды |
| **operator (BlackRoad-OS)** | https://github.com/BlackRoad-OS-Inc/operator | Полный контекст BlackRoad OS для людей и машин — context-first OS | 3 | 2 звезды |
| **open-workspace (pajew-ski)** | https://github.com/pajew-ski/open-workspace | Local-first когнитивный workspace с A2A, A2UI, MCP протоколами и локальным Ollama | 3 | 2 звезды |
| **spectre (12georgiadis)** | https://github.com/12georgiadis/spectre | "Призрак над shell" — claude-code-workflow от filmmaker | 3 | 0 звезд |
| **Awesome Claude Code** | https://github.com/hesreallyhim/awesome-claude-code | Курированный список скиллов, хуков, команд, оркестраторов, плагинов для Claude Code | 3 | <500 звезд |
| **claude-code-workflows (shinpr)** | https://github.com/shinpr/claude-code-workflows | Production-ready development workflows для Claude Code со специализированными AI-агентами | 3 | <200 звезд |
| **Dsebastien AKM** | https://www.dsebastien.net/agentic-knowledge-management-the-next-evolution-of-pkm/ | Концепция Agentic KM: AI наблюдает за knowledge base и предлагает действия, не ожидая команд | 3 | Блог/концепт |

---

## Категория 4 — Vendor-agnostic AI environments

> Решения, абстрагирующие AI-вендора: единый интерфейс, сохранение контекста при смене модели

| Название | URL | Описание (1 предложение) | Категория | Размер |
|----------|-----|--------------------------|-----------|--------|
| **LiteLLM** | https://github.com/BerriAI/litellm | Единый интерфейс для 100+ LLM API с gateway, load balancing, audit logs | 4 | 20k+ звезд |
| **any-llm (Mozilla)** | https://github.com/mozilla-ai/any-llm | Mozilla Python SDK: единый интерфейс для переключения между LLM одной строкой | 4 | <500 звезд |
| **Onyx** | https://github.com/onyx-dot-app/onyx | Open-source AI-платформа: универсальная LLM-совместимость, enterprise knowledge base | 4 | 10k+ звезд |
| **Jan App** | https://github.com/janhq/jan | Offline ChatGPT-альтернатива: десктоп, локальные LLM, OpenAI-совместимый API | 4 | 30k+ звезд |
| **CX Linux** | https://github.com/cxlinux-ai/cx-core | AI-powered Linux OS: системное администрирование на естественном языке (Rust) | 4 | 49 звезд |
| **Bifrost** | https://bifrost.ai | AI-шлюз: 15+ LLM провайдеров через единый OpenAI-совместимый API, failover, governance | 4 | Коммерческий |
| **OpenRouter** | https://openrouter.ai | Единый API-роутер для 100+ LLM: переключение моделей, cost routing, automatic fallback | 4 | Коммерческий |
| **AppFlowy** | https://github.com/AppFlowy-IO/AppFlowy | Open-source Notion-альтернатива с AI, offline-first, данные принадлежат пользователю | 4 | 65k+ звезд |
| **AFFiNE** | https://github.com/toeverything/AFFiNE | Local-first knowledge base: markdown + whiteboard + AI, privacy-first open-source | 4 | 37.8k звезд |
| **TriliumNext** | https://github.com/triliumnext/Notes | Community-форк Trilium Notes: иерархические заметки, self-hosted, backward-compatible | 4 | 5k+ звезд |

---

## Дополнительные — PKM-инструменты (фундаментальный слой)

> Инструменты, на которых строятся многие аналоги IWE

| Название | URL | Описание (1 предложение) | Категория | Размер |
|----------|-----|--------------------------|-----------|--------|
| **Obsidian** | https://obsidian.md | Markdown PKM с граф-связями, плагинами, Vault = локальные файлы пользователя | PKM | 10M+ users |
| **Logseq** | https://github.com/logseq/logseq | Open-source outliner-PKM: Markdown/Org-mode, bidirectional links, полностью локальный | PKM | 35k+ звезд |
| **Foam** | https://github.com/foambubble/foam | VS Code-расширение: Roam-подобный PKM поверх Markdown файлов | PKM | 15k+ звезд |
| **Zk** | https://github.com/zk-org/zk | CLI plain-text note-taking assistant с Zettelkasten методологией | PKM | 2.5k звезд |
| **Notabase** | https://github.com/churichard/notabase | Second brain для знаний, мыслей и идей с bidirectional links | PKM | 901 звезда |
| **Revezone** | https://github.com/revezone/revezone | Lightweight local-first графически-ориентированный productivity tool | PKM | 2.6k звезд |
| **Nocturne Memory** | https://github.com/Dataojitori/nocturne_memory | Lightweight, rollbackable, visual Long-Term Memory Server для MCP агентов | PKM | 886 звезд |

---

## Статистика

| Категория | Проектов | Малоизвестных (<1000 звезд) |
|-----------|----------|----------------------------|
| 1 — Прямые аналоги (экзокортексы) | 24 | 14 |
| 2 — AI-обёртки и оркестраторы | 14 | 6 |
| 3 — Structured AI workflows | 13 | 11 |
| 4 — Vendor-agnostic | 10 | 2 |
| PKM-слой (фундаментальный) | 7 | 4 |
| **ИТОГО** | **68** | **37** |

---

## Особо ценные находки (малоизвестные, близки к IWE по духу)

Проекты, наиболее близкие к концепции IWE (методология + файлы + AI-агент):

1. **ZK Context Vault** (2 звезды) — 7-слойная когнитивная инфраструктура с exocortex, slice-архитектурой, principles layer — прямой архитектурный аналог IWE
2. **Strategy-OS** (23 звезды) — validation layer для соло-фаундеров на Claude Code, структурированные протоколы-gates
3. **Ars Contexta** (2.9k) — Claude Code плагин: персональная knowledge-система через разговор, 6-фазный pipeline
4. **fuwasegu/exocortex** (<20) — централизованный экзокортекс для девелопера, privacy-first, semantic search паттернов
5. **forkwright/aletheia** (1) — "distributed cognition system, infrastructure and continuity"
6. **open-workspace (pajew-ski)** (2) — A2A+A2UI+MCP local-first cognitive workspace
7. **t9os** (2) — философская OS для AI-человеческой индивидуации на Claude Code
8. **embraOS** (1) — continuity-preserving AI OS, эволюция через время
9. **ARI** (5) — 7-уровневая архитектура с LOGOS/ETHOS/PATHOS когницией и аудитом
10. **operator (BlackRoad-OS)** (2) — "full context for humans and machines"
11. **Daniel Rosehill AI workspace** (<50) — 1000+ system prompts + Agent Studio концепция
12. **LC-OS-Project** (4) — practitioner toolkit для AI workflow adoption
13. **exocortex-halo (virtadpt)** (76) — реальный working exocortex на Huginn, ветеранский проект
14. **PAI (danielmiessler)** (11k) — глубокая методология TELOS, 6 слоёв персонализации, closest large-scale analogue
15. **Daniel Rosehill System-Prompt-Library** — 1290 system prompts, ecosystem approach to personal AI configuration

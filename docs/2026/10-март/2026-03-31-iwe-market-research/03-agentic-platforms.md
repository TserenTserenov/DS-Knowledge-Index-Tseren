# Кластер: Agentic AI Platforms

**Дата среза:** 31 марта 2026

Системы для knowledge workers с агентным слоем. Акцент: инфраструктура и польза, не функции.

---

<details open>
<summary><b>Dust.tt — Infrastructure-First AI OS for Teams (ближайший по философии)</b></summary>

**URL:** https://dust.tt | **GitHub:** https://github.com/dust-tt/dust (открытый репозиторий)
**Финансирование:** Sequoia backed. $7M+ ARR (2024). ~98 сотрудников к 2026. Основан февраль 2023, Париж.
**Позиционирование:** "AI Operating System for Work" — их собственный термин.

### Польза для knowledge worker

80 000 агентов создано пользователями к 2025. Один PM создал 242 агента. Risk agent — 2.09 млн сообщений для fintech compliance. Support agent видит Zendesk + docs одновременно. RevOps — Slack + Salesforce + Gong в одном запросе.

### Инфраструктура

**Tech stack:**
- Frontend: Next.js + TypeScript
- Backend: Rust-based internal services (сознательный отход от Python)
- Orchestration: **Temporal** (cloud) — 10+ млн Temporal Activities в день
- DB: PostgreSQL + Google Cloud Storage
- Models: multi-model (GPT-4o, Claude 3.5 Sonnet, DeepSeek, o3-mini, Gemini)

**Почему Temporal:** каждое входящее событие (Slack message → ticket, PR → code review, doc update → re-index) запускает Temporal Workflow. Long-running задачи (chunking, embeddings, API polling) = Temporal Activities с retry-логикой и state persistence. Это решает проблему агентных задач > 30 секунд.

**RAG-архитектура:** собственные коннекторы (не Airbyte) к: Slack, Google Drive, Notion, Confluence, GitHub, Gong, Gmail, Google Calendar, Salesforce, HubSpot, Linear, Outlook, SharePoint, Zendesk, BigQuery. Причина собственных коннекторов: LLM-специфичная обработка требует правильного чанкинга под контекстные окна.

**Human-in-the-loop (4 уровня):**
1. Admin → какие MCP-серверы доступны в workspace
2. User → фильтрация инструментов для своего агента
3. LLM → выбор из отфильтрованного набора
4. **Runtime override** → approve/reject конкретного tool call ДО исполнения

**Memory (с 2025):** persistent agent memory — агенты запоминают preferences, ongoing projects, past interactions across ALL conversations. **Tracker product** (2025): мониторит stale documentation и предлагает обновления prompt'ов агентов — "agent-for-agents" паттерн.

**Агент chaining (2025):** research agent → writing agent параллельно. Triggered agents (из GitHub, Jira, Zendesk). Scheduled agents (без инициации человеком).

**Бизнес-модель:** Pro €29/user/month. Enterprise: custom (SSO Okta/Entra, SCIM, US/EU data hosting).

### Разрыв с IWE

Нет структурных ритуалов работы (ОРЗ-фрактал). Human-in-the-loop = approval per tool call, а не протокол сессии. Нет Pack-архитектуры (source-of-truth иерархии). Нет мультипликатора. Командный, а не личный инструмент.

**Ключевые архитектурные публикации:**
- https://temporal.io/blog/how-dust-builds-agentic-ai-temporal
- https://www.zenml.io/llmops-database/building-a-horizontal-enterprise-agent-platform-with-infrastructure-first-approach
- https://dust.tt/blog/mcp-and-enterprise-agents-building-the-ai-operating-system-for-work

</details>

---

<details>
<summary><b>Glean — Enterprise Knowledge Graph + Adaptive Planning</b></summary>

**URL:** https://www.glean.com
**Финансирование:** Series F, $150M (июнь 2025). Оценка ~$4.6B. Sales-led enterprise.

### Польза

"Layer beneath the interface" — контекстный слой поверх которого работают агенты. 100+ коннекторов. Агент cross-domain: знает одновременно людей, команды, процессы, активности.

### Инфраструктура

**Agentic Engine 2 (Fall 2025):**
- **Adaptive planning** — агент непрерывно перепланирует (не waterfall)
- Sub-agents: parallel runners + "Scouts" для обнаружения новой информации
- Sandbox environment: isolated filesystem + code runtime + indexed search (обходит лимиты контекста)
- Метрики: 94% task completeness (+21% usage vs Engine 1)

**Enterprise Graph v3 (Fall 2025):** live, permission-aware карта организации. People + Teams + Processes + Activities. **Personal Graph:** индивидуальный подход каждого пользователя к работе. 3x больше сигналов чем v2.

**Memory:** Enterprise Graph = "full long-term memory". История агентных работ + enterprise-wide activities + Personal Graph.

**Бизнес-модель:** $50+/user/month, минимум 100 seats. Медианный контракт ~$65K/год. Enterprise deal $200K+.

### Разрыв с IWE

Только enterprise (не personal). Нет ритуалов работы. Нет Pack-архитектуры. Нет мультипликатора. Нет git-native.

**Ключевые публикации:**
- https://www.glean.com/blog/emerging-agent-stack-2026
- https://www.glean.com/blog/live-fall-25-agentic-engine2-performance

</details>

---

<details>
<summary><b>Slashy (YC S25) — "Cursor for Knowledge Workers"</b></summary>

**URL:** https://slashy.ai | YC S25
**Финансирование:** $500K seed (Afore Capital, Exitfund, Link Ventures, Pioneer Fund)
**Позиционирование:** буквально называют себя "Cursor for knowledge workers"

### Польза

Единый агент для: meeting preparation, JIRA ticket creation, CRM updates, note-taking, email management. 15+ сервисов в одном интерфейсе. Custom UI для каждой интеграции.

### Инфраструктура

**Архитектурные решения (по HN Launch thread):**
- **Single agent architecture** (сознательный выбор против multi-agent) → снижение галлюцинаций при передаче контекста
- **Не используют MCP**: собственные tool implementations. Обоснование: "качество MCP-инструментов пока недостаточно для parallel use"
- AWS + Claude/OpenAI (main agent) + Groq (tool routing — для скорости)
- OAuth-based credential management
- Semantic indexing "similar to Glean but without ACLs"

**Интеграции:** G-Suite, Slack, Notion, Dropbox, Airtable, Outlook, Linear, HubSpot.

### Разрыв с IWE

Нет knowledge management. Нет ритуалов. Нет Pack-архитектуры. Нет памяти между сессиями (пока). Ранняя стадия.

**Ключевая ссылка:** https://news.ycombinator.com/item?id=45129031 (архитектурные детали от основателей)

</details>

---

<details>
<summary><b>Minro (YC S25) — Behavioral Replication Agent</b></summary>

**YC Batch:** S25 | **Продукт:** Iris (calendar + email agent)

### Ключевая идея

**Принципиально другой подход:** наблюдение за тем КАК пользователь работает → репликация суждения, не только задач. "Если смоделировать реальное поведение, можно реплицировать judgment, не только tasks."

### Инфраструктура

Knowledge graph как personal behavioral model. 1200+ downloads, 168 DAU, 36 000+ actions, рост 48% WoW (YC Demo Day).

**UX:** swipe right → агент берёт действие. Pre-fills actions на основе наблюдаемых паттернов.

### Разрыв с IWE

Ранняя стадия. Только email + calendar (узко). Нет PKM. Нет ритуалов. Нет Pack. Нет мультипликатора.

**Источник:** https://insights.tryspecter.com/yc-requested-startups-fall-2025/

</details>

---

<details>
<summary><b>Lindy AI — No-Code Agent Automation</b></summary>

**URL:** https://www.lindy.ai
**Бизнес-модель:** Free (400 кредитов) / Pro $29.99/мес / Business custom. 4000+ интеграций.

### Польза

Email triage, lead qualification, content moderation, research — через visual workflow builder. Multi-agent collaboration нативно: один agent qualifies leads → другой sends follow-ups → третий updates CRM.

### Инфраструктура

LLM-based reasoning (не if-then, как Zapier). Parallel execution: один агент дублирует себя для массовых задач. Vector database для knowledge retention. 4000+ интеграций через Zapier-подобный слой.

### Разрыв с IWE

Нет PKM. Нет ритуалов. Нет Pack-архитектуры. Нет мультипликатора. Нет git-native. Это workflow automation, не операционная система мышления.

**Ключевая ссылка:** https://www.lindy.ai/blog/ai-agent-architecture

</details>

---

<details>
<summary><b>Microsoft 365 Copilot Agents — Enterprise Standard</b></summary>

**URL:** https://adoption.microsoft.com/en-us/ai-agents/copilot-studio/
**Бизнес-модель:** M365 Copilot $30/user/мес + Copilot Studio $200/мес (25K сообщений)

### Инфраструктура

**Два типа агентов:**
- **Declarative agents:** кастомизируют M365 Copilot через instructions + actions + knowledge. No-code Agent Builder или VS Code.
- **Autonomous agents (Copilot Studio):** multi-step processes independently.

**Microsoft Agent 365:** единый control plane. AI agents как **security principals** с identity, permissions, audit trail. Admin pre-approval для trusted agents. Lifecycle hooks. Escalation paths.

**Knowledge:** People as knowledge source (org chart, roles, reporting). SharePoint, OneDrive, Teams + внешние MCP-серверы (март 2025: MCP support).

**Memory:** Microsoft Graph как organizational memory. Session context + cross-app history.

### Разрыв с IWE

Enterprise = не personal. Нет ритуалов. Нет Pack-архитектуры. Нет мультипликатора. Нет git-native. Vendor lock-in.

**Ключевые ссылки:**
- https://devblogs.microsoft.com/microsoft365dev/build-declarative-agents-for-microsoft-365-copilot-with-mcp/
- https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/09/powering-frontier-transformation-with-copilot-and-agents/

</details>

---

<details>
<summary><b>Fibery, Coda, Guru, ClickUp Brain — Workspace-Native Agents</b></summary>

### Fibery
**URL:** https://fibery.com | Seed $3.1M. MRR +85% при сокращении маркетинга на 85% — сильный PMF-сигнал.

**Инфраструктура:** work management + knowledge management в одном. **Highlights** — гибрид database + knowledge graph. AI Context (фев. 2026): агент знает имена всех Databases, Views, Rules. **Architect mode** (янв. 2026): AI помогает конфигурировать саму систему. Стратегия 2026: "safest agent-operable Company OS".

**Ключевая ссылка:** https://community.fibery.io/t/fibery-strategy-2026/10170

---

### Coda Brain
**URL:** https://coda.io | Pro $10/мес per Doc Maker

**Инфраструктура:** **Coda Brain** — Snowflake + 500+ tool integrations. Natural language → automatic SQL. AI включён в планы (не доп. плата, как у Notion/ClickUp). Packs: живые данные из HubSpot, Google Analytics, Salesforce, Jira.

---

### Guru
**URL:** https://www.getguru.com | $15-20/user/мес

**Инфраструктура:** **Governed knowledge layer** с верификацией. При обновлении эксперта — propagation across every workflow. Federated Search (2026): индексирование Google Drive + Box без миграции. MCP support: другие AI используют Guru как knowledge source. **Verification workflow** = human-in-the-loop по умолчанию.

---

### ClickUp Brain / Super Agents
**URL:** https://clickup.com/brain | Free-$12/мес

**Инфраструктура:** Neural network layer поверх workspace. Multi-model (GPT-5, Claude Opus 4.1, o3). **Super Agents** (2025-2026): видят tasks + docs + chats + meetings + schedules. 24/7 autonomous operation.

</details>

---

## Паттерны кластера: что объединяет и разделяет

**Архитектурный консенсус (все делают одинаково):**
- RAG поверх корпоративных данных
- Multi-model (не lock-in на одну модель)
- MCP как стандарт интеграции (кроме Slashy — принципиально против)
- Approval gates как human-in-the-loop

**Архитектурные развилки (где расходятся):**

| Решение | Сторонники | Критики |
|---------|-----------|---------|
| Single agent | Slashy (меньше галлюцинаций) | Все остальные (параллелизм) |
| Собственные коннекторы | Dust, Glean (качество чанкинга) | Lindy, ClickUp (скорость) |
| Persistent memory | Dust, Glean (cross-session) | Большинство (stateless) |
| Temporal orchestration | Dust (long-running tasks) | Нигде больше не упоминают |

**Белое пятно всего кластера:** ни один продукт не реализует **structured work rituals** — ОРЗ-фрактал с явными протоколами открытия и закрытия на масштабах сессии/дня/недели. Human-in-the-loop везде = "approve action", а не "участие в методологии работы".

**YC S25 сигнал:** ~50% батча — agentic AI. Тренд от workflow automation → к behavioral replication (Minro). Это ближе к IWE-концепции, но в ранней стадии.

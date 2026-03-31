# Матрицы бенчмарка

**Дата среза:** 31 марта 2026
**Метод:** SOTA-покрытие (13 практик) + Функциональный профиль IWE (L1–L5) + ЭМОГССБ (7 характеристик)

Шкала: ✓ реализовано / ~ частично / — отсутствует | Для ЭМОГССБ: 1–10

---

## 1. SOTA-матрица (продукт × практика)

| Продукт | S001 DDD | S002 CtxEng | S003 MCP | S004 GraphRAG | S005 AI-Org | S006 Agentic | S007 Ontology | S008 Capture | S009 DigTwin | S011 Coupling | S012 Multi-Repr | Итог |
|---------|----------|-------------|----------|---------------|-------------|--------------|---------------|--------------|--------------|--------------|----------------|------|
| **IWE** | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ~ | ✓ | ~ | ✓ | ~ | **10/13** |
| Tana | ~ | ~ | — | ✓ | ~ | ~ | ~ | ✓ | — | — | — | 4/13 |
| Notion 3.0 | — | ~ | ~ | — | ✓ | ✓ | — | ~ | — | — | — | 4/13 |
| Dust.tt | — | ✓ | ✓ | — | ✓ | ✓ | — | ~ | — | ~ | — | 5/13 |
| Glean | ~ | ✓ | ~ | ✓ | ✓ | ✓ | — | — | ~ | ~ | ~ | 7/13 |
| Letta | — | ✓ | ~ | — | ✓ | ✓ | — | ✓ | — | — | — | 5/13 |
| Mem0 | — | ✓ | — | ✓ | — | ~ | — | ✓ | — | — | ~ | 4/13 |
| Zep/Graphiti | — | ✓ | ✓ | ✓ | — | ~ | — | ✓ | — | — | ~ | 5/13 |
| Obsidian | — | — | ✓ | — | — | — | — | ✓ | — | — | — | 2/13 |
| Logseq | — | — | — | ~ | — | — | — | ✓ | — | — | — | 1/13 |
| Slashy | — | ~ | — | — | — | ~ | — | — | — | — | — | 1/13 |
| M365 Copilot | — | ~ | ✓ | ~ | ✓ | ✓ | — | — | — | — | — | 4/13 |
| Khoj | — | ~ | ~ | — | — | ~ | — | ✓ | — | — | — | 2/13 |

**Расшифровка SOTA:**
S001=DDD Strategic, S002=Context Engineering, S003=MCP/OpenAPI, S004=GraphRAG+KG, S005=AI-Native Org, S006=Agentic Dev, S007=AI Ontology, S008=RT Capture, S009=Digital Twin, S011=Coupling Model, S012=Multi-Repr

---

## 2. Функциональный профиль IWE (L1–L5)

| Продукт | L1 PKM | L2 Агенты | L3 ОРЗ-ритуалы | L4 Мультипликатор | L5 Экосистема | Профиль |
|---------|--------|-----------|----------------|-------------------|---------------|---------|
| **IWE** | ✓ | ✓ | ✓ | ✓ | ✓ | **5/5** |
| Tana | ✓ | ~ | ~ | — | ~ | 3/5 |
| Notion 3.0 | ✓ | ✓ | — | — | ~ | 3/5 |
| Obsidian | ✓ | — | — | — | ~ | 2/5 |
| Dust.tt | — | ✓ | — | — | ✓ | 2/5 |
| Glean | — | ✓ | — | — | ✓ | 2/5 |
| Letta | — | ✓ | — | — | — | 1/5 |
| Mem0 | — | ~ | — | — | — | 0.5/5 |
| Zep/Graphiti | — | ~ | — | — | — | 0.5/5 |
| Logseq | ✓ | — | — | — | ~ | 1.5/5 |
| Khoj | ✓ | ~ | — | — | ~ | 1.5/5 |
| Slashy | — | ~ | — | — | ~ | 0.5/5 |
| M365 Copilot | — | ✓ | — | — | ✓ | 2/5 |
| COG second brain | ✓ | ~ | — | — | ✓ | 2/5 |

**Ключевые наблюдения:**
- L3 (ОРЗ-ритуалы) = **абсолютно уникален**. Tana — частичная реализация (Daily Page), все остальные — нет.
- L4 (Мультипликатор) = **только IWE**. Нигде больше нет концепции физическое→интеллектуальное с измеримым коэффициентом.
- L2 (Агенты) = у Notion 3.0 и Dust самый зрелый слой.
- L1+L5 без L2–L4 = инструмент, не ОС.

---

## 3. ЭМОГССБ-профили

### IWE

| Хар-ка | Оценка | Обоснование |
|--------|--------|-------------|
| **Э** Эволюционируемость | 9 | L1/L2/L3 слои разделены. update.sh = platform update без потери авторского. Extensions gate. |
| **М** Масштабируемость | 7 | Масштаб от сессии до недели. Ограничение: персональный инструмент, не командный. |
| **О** Обучаемость | 8 | AutoMemory + AutoDream. Протоколы эволюционируют через staging→promotion. |
| **Г** Генеративность | 9 | Capture-to-Pack на каждом рубеже. Pack = растущая база доменного знания. |
| **С** Скорость | 7 | Быстрые протоколы (Quick Close). Ограничение: ручные ритуалы требуют времени. |
| **С** Современность | 9 | MCP + SOTA.002 Context Engineering + Agentic Development (SOTA.006). |
| **Б** Безопасность | 9 | Local-first (git). Нет vendor lock-in. Данные под контролем пользователя. |
| **Итог** | **8.3** | Проходит порог ≥8 |

---

### Notion 3.0

| Хар-ка | Оценка | Обоснование |
|--------|--------|-------------|
| **Э** | 5 | Полное пересоздание стека (2025) — нет backward compatibility гарантий. |
| **М** | 9 | 30M пользователей. Multi-team. Enterprise scale. |
| **О** | 7 | Agents учатся из workspace. Page-as-memory. Нет явного feedback loop. |
| **Г** | 8 | Agents создают docs, databases, workflows автономно. |
| **С** | 7 | 20-минутные автономные задачи. Но cloud latency. |
| **С** | 8 | Multi-model (GPT-5/Claude/Gemini). Agents. MCP (beta). |
| **Б** | 4 | Cloud-only. Vendor lock-in. Данные на серверах Notion. |
| **Итог** | **6.9** | Не проходит порог ≥8 (особенно Б и Э) |

---

### Tana

| Хар-ка | Оценка | Обоснование |
|--------|--------|-------------|
| **Э** | 6 | Supertags как расширяемая схема. Но нет separating concerns между platform и user layer. |
| **М** | 7 | Cloud-based graph. Оффлайн добавлен. 160K+ waitlist = рост. |
| **О** | 7 | Daily Page с AI = proto-ritual. AI-поля учатся из Supertag-паттернов. |
| **Г** | 7 | Knowledge graph = explicit связи. Supertag-конфигурируемые agents. |
| **С** | 6 | Нет explicit feedback на скорость работы. |
| **С** | 7 | Мультипровайдер AI. Нет MCP. Voice. |
| **Б** | 5 | Cloud-only. Proприетарный граф. Нет self-hosted. |
| **Итог** | **6.4** | Не проходит порог ≥8 |

---

### Dust.tt

| Хар-ка | Оценка | Обоснование |
|--------|--------|-------------|
| **Э** | 8 | Open-source + Temporal workflows. Builders могут кастомизировать без engineering. |
| **М** | 8 | Enterprise-scale. 10M+ Temporal Activities/день. Multi-team. |
| **О** | 7 | Persistent memory (2025). Tracker = self-updating agents. |
| **Г** | 7 | 80K агентов созданы пользователями. Но командный, не personal. |
| **С** | 8 | Temporal = async long-running tasks без timeout. P95 latency не раскрывается. |
| **С** | 8 | Rust backend. Temporal. Multi-model. MCP. Context Engineering применён. |
| **Б** | 7 | Cloud (US/EU choice). Нет self-hosted. Open-source code = аудируем. |
| **Итог** | **7.6** | Близко к порогу, но не достигает ≥8 |

---

### Letta

| Хар-ка | Оценка | Обоснование |
|--------|--------|-------------|
| **Э** | 9 | Open-source. Pluggable memory backends. Letta V1 = backward-breaking, но с migration path. |
| **М** | 7 | Self-hosted + cloud. Multi-agent namespacing. |
| **О** | 9 | Агент сам управляет памятью. Core/Recall/Archival = explicit learning. |
| **Г** | 6 | Инфраструктура, не end-user product. |
| **С** | 7 | Overhead на tool calls для memory management. |
| **С** | 8 | MemGPT paper = pioneering. Letta V1 = modern LLM support. |
| **Б** | 9 | Self-hosted (AGPL). Full data ownership. |
| **Итог** | **7.9** | Близко, но не достигает ≥8 (drag от Г и С) |

---

## 4. Сводная матрица: что только у IWE

| Концепция | IWE | Ближайший аналог | Разрыв |
|-----------|-----|-----------------|--------|
| ОРЗ-фрактал (три масштаба) | ✓ | Tana Daily Page (~) | Нет Закрытия, нет Недели |
| Pack-архитектура (source-of-truth иерархия) | ✓ | Tana Supertags (~) | Нет fallback chain DS→Pack→Base |
| Мультипликатор (физическое→интеллектуальное) | ✓ | Нигде | Уникальная концепция |
| Git-native для knowledge | ✓ | Obsidian (через плагин) | Не нативный |
| Агентные роли + context isolation | ✓ | Dust (builder roles) | Нет session isolation |
| Self-correction протокол | ✓ | Нигде | Уникальная концепция |
| WP Gate (рабочий продукт перед работой) | ✓ | Нигде | Уникальная концепция |
| Staged rollout (staging → platform) | ✓ | Нигде | Уникальная концепция |
| Priority Gate (к какому R{N} ведёт РП) | ✓ | Нигде | Уникальная концепция |
| Local-first + agent layer | ✓ | COG second brain (~) | Нет методологии поверх |

**Итог бенчмарка:** IWE = единственная система с полным профилем L1–L5. SOTA-покрытие 10/13 vs максимум 7/13 у ближайшего конкурента (Glean). ЭМОГССБ: 8.3 — проходит архитектурный порог.

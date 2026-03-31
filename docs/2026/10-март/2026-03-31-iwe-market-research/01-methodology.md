# Методология исследования

**Дата среза:** 31 марта 2026
**Цель:** аналитическое сравнение продуктов-аналогов IWE для понимания рынка и позиционирования

---

## Что такое IWE

IWE (Intellectual Work Environment) — персональная операционная система для интеллектуальной работы. Аналог IDE, но не для кода, а для мышления. Включает:

- **PKM-слой** (Pack-архитектура: source-of-truth иерархия DS→Pack→Base)
- **Агентный слой** (роли, скиллы, протоколы с context isolation)
- **Операционный слой** (ОРЗ-фрактал: Открытие→Работа→Закрытие на масштабах сессии/дня/недели)
- **Рабочие продукты** (РП как артефакты с явными бюджетами времени)
- **Мультипликатор** (физическое время → интеллектуальный output, целевой коэффициент 2x+)

---

## Оси бенчмарка

### Ось 1: SOTA-покрытие (SOTA.001–SOTA.013)

Оценка того, какие современные практики реализованы в продукте:

| ID | Практика |
|----|---------|
| SOTA.001 | DDD Strategic (bounded contexts, ubiquitous language) |
| SOTA.002 | Context Engineering (write/select/compress/isolate) |
| SOTA.003 | Open API Specs (MCP, стандартные контракты) |
| SOTA.004 | GraphRAG + Knowledge Graph |
| SOTA.005 | AI-Native Org Design (роли агентов) |
| SOTA.006 | Agentic Development (multi-agent, IPO-паттерн) |
| SOTA.007 | AI-Accelerated Ontology |
| SOTA.008 | Real-Time Knowledge Capture |
| SOTA.009 | Knowledge-Based Digital Twins |
| SOTA.010 | DSL → DSLM Evolution |
| SOTA.011 | Coupling Model (knowledge/distance/volatility) |
| SOTA.012 | Multi-Representation Architecture |
| SOTA.013 | SAI / Evolvability (LeCun 2026) |

Шкала: ✓ реализовано / ~ частично / — отсутствует

### Ось 2: Функциональный профиль IWE (L1–L5)

| Слой | Что измеряем |
|------|-------------|
| L1 | PKM / Knowledge Storage |
| L2 | Агентный слой (роли, протоколы, скиллы) |
| L3 | Операционный слой (ОРЗ-ритуалы, рабочие продукты) |
| L4 | Мультипликатор (физическое → интеллектуальный output) |
| L5 | Экосистемный слой (интеграции, git-native, cross-repo) |

### Ось 3: ЭМОГССБ-профиль (архитектурные характеристики)

| Буква | Характеристика |
|-------|---------------|
| Э | Эволюционируемость (можно ли менять без слома) |
| М | Масштабируемость |
| О | Обучаемость (агент учится на опыте) |
| Г | Генеративность (создаёт новое знание) |
| С | Скорость (latency, feedback loops) |
| С | Современность (SOTA-соответствие) |
| Б | Безопасность (data ownership, privacy) |

Шкала 1–10. Порог ≥8 для архитектурного решения.

### Ось 4: Пользовательская ценность

Три вопроса на каждый продукт:
1. **Польза** — что конкретно решает для knowledge worker?
2. **Инфраструктура** — как устроено внутри (data layer, agent layer, memory)?
3. **Разрыв с IWE** — чего не хватает принципиально?

---

## Источники

**Академические:** arxiv.org, ACL Anthology, Royal Society of Chemistry Digital Discovery, CHI/NeurIPS/EMNLP proceedings

**Открытые публикации:** Simon Willison (simonwillison.net), Lilian Weng (lilianweng.github.io), Maggie Appleton (maggieappleton.com), Eugene Yan (eugeneyan.com), Latent Space (latent.space), ZenML LLMOps Database

**GitHub:** звёзды, коммиты, issues — как прокси активности

**Community:** Hacker News, ProductHunt, YC directory, r/PKMS, r/ObsidianMD

**Коммерческие данные:** TechCrunch, VentureBeat, CB Insights, Crunchbase

---

## Таксономия кластеров

```
IWE-пространство
├── PKM + AI          (Obsidian, Notion, Tana, Capacities, Heptabase, Logseq, Mem.ai...)
├── Agentic Platforms (Dust, Glean, Lindy, Slashy, Notion Agents, M365 Copilot...)
├── Memory Infra      (Letta, Mem0, Zep, LangMem, Khoj, COG second brain...)
└── Academic & Proto  (MemOS, OpenDAN, Dreamer, COG second brain, BASB AI pivot...)
```

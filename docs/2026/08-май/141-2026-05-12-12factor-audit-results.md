---
type: post
title: "Когда `git push` ничего не деплоит: 12-factor ревизия моей AI-экосистемы"
audience: advanced
status: draft
created: 2026-05-12
target: club
channel_number: 1
post_number: 141
source_knowledge: "WP-307 12factor-compliance audit"
tags: [12factor, cloud-native, audit, ai-ecosystem, self-review]
content_plan: "WP-307"
---

# Когда `git push` ничего не деплоит: 12-factor ревизия моей AI-экосистемы

Несколько месяцев я строил AI-агентную экосистему — боты, MCP-серверы, projection-workers, edge-функции. Каждый сервис делался под конкретную задачу, без единого инженерного стандарта. Сегодня я провёл первую системную ревизию по [12 факторам Heroku](https://12factor.net/) — методология cloud-native гигиены, на которой держится индустрия с 2011 года. Это срез того, что у меня вышло за полгода активной разработки.

Если коротко: **функционально готово к когорте 50 пользователей; операционно — фундамент дырявый.**

## Что проверяли

Production runtime — это **28 deployment units** (думал, что 10):

- 2 Telegram-бота (prod + pilot) на Railway
- 6 background workers (event-poller, projection-workers, activity-hub, payment-registry)
- 11 Cloudflare Workers (gateway, knowledge-MCP, personal-MCP, digital-twin-MCP, FSM, guides, events, observability, payments, status, google-drive)
- 6 autonomous agents (auditor, profiler, strategist и др.) на tsekh-1
- Локальный gateway, OAuth Hydra, CRM, backup-инфра, статичный сайт
- Admin-скрипты (Neon migrations)

12 факторов × 28 сервисов = **336 ячеек compliance-матрицы.**

## Метод

Линейный аудит по факторам (подход A): одна фаза на фактор, ~0.5-3h каждая. Всего ~12h фактической работы (vs бюджет 60h — оценка оказалась завышена в 5 раз). Каждый фактор: grep по коду, проверка Dockerfile/manifest/config, заполнение матрицы.

Verify-стадия — sub-agent в изолированном контексте (Sonnet) с эталоном 12factor.net. И второй independent reviewer на финале. Trust-but-verify работает только если verify реально independent.

## Главные находки

### 🚨 F5 BRR — 20 сервисов из 28 в красной зоне

Самая жёсткая находка пришла случайно — на фазе Ф9 (Disposability). Решил посмотреть env vars одного Railway-воркера. Нет `RAILWAY_GIT_COMMIT_SHA`. Ни в одном из пяти. Проверил deploy history — везде `reason: "deploy"/"redeploy"` (manual triggers), не `"github"`. Push в `main` не триггерит ничего. Workers деплоились через `railway up` с локальной машины. Последний successful deploy одного из них — 28 апреля. Сегодня 12 мая. **Между ними две недели коммитов, которых в проде нет.**

Поднял на следующий уровень: а CF Workers? У них же должен быть `wrangler-action` в GitHub Actions, это же стандарт. Проверил `.github/workflows/` в 10 репозиториях. В четырёх — только `secret-scan.yml` + `security.yml`. В шести — нет `.github` директории вообще. `wrangler deploy` запускается локально. Каждый из них.

Итого: **15 production-сервисов без CI deploy.** Image immutable digest есть (Railway), V8 snapshot version_id есть (CF Workers) — но git→deploy linkage отсутствует. Нельзя сказать, какой commit в проде. Нельзя rollback к конкретному SHA. Любая security-разборка займёт часы вместо минут.

В аудите это понизило F5 для 15 сервисов с ✅ до ❌, и F1 (Codebase) — с ✅ до ⚠️.

### ✅ F6 Stateless — единственный фактор, готовый к масштабированию

Здесь, наоборот, приятно. Бот переехал с MemoryStorage на PostgresStorage (FSM-state в БД). Все 4 worker'а — на DB-cursor с per-domain isolation и batched flush. CF Workers stateless by design. **19 из 28 — ✅, ни одного ❌.** Архитектура готова к R1→R2→R3 без рефакторинга stateful-частей.

### 🔒 F3 Config — 0 hardcoded secrets

Прогрепал HEAD-код всех сервисов на Telegram-токены, API-ключи, `sk-`/`pk-` префиксы. **Ни одного hardcoded secret.** Культура «всё через env var» соблюдается. Проблемы только в `.gitignore` гигиене (4 сервиса без `.env` правила) и отсутствии `.env.example` для onboarding (10 сервисов).

### ✅ F8 Concurrency — закрыто mitigation

W2/W3 (poller + multi-domain projection) — single-replica de-facto, но контракт не был задокументирован. Случайный `railway scale 2` сломал бы event-ingestion дублями. Закрыли через `pg_try_advisory_lock(key)` на shared learning DB + SCALING.md с явным контрактом. Дешёвый и надёжный паттерн для будущих stateful Railway workers.

### ✅ F9 Disposability — production workers все ✅

Все 4 Railway worker'а и оба бота имеют явный SIGTERM handler через `loop.add_signal_handler(signal.SIGTERM, stop_event.set)`. Cursor-based idempotency защищает от crash/retry дублей. CF Workers — <100ms cold start (V8 isolates), request-isolated.

## Полная таблица 28 × 12

> Легенда: ✅ соблюдён · ⚠️ соблюдён частично · ❌ нарушен · 🟡 TBD (legit pending) · N/A неприменим

| Сервис | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 |
|--------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| B1 aist-bot prod | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| B2 aist-bot pilot | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| W1 activity-hub | ⚠️ | ⚠️ | ✅ | ✅ | ❌ | ✅ | N/A | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| W2 bridge-2-events-poller | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ | N/A | ✅ | ✅ | ⚠️ | ✅ | N/A |
| W3 multi-domain-projection-worker | 🟡 | ⚠️ | ⚠️ | ✅ | 🟡 | ✅ | N/A | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| W4 rewards-projection-worker | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ | N/A | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| W5 payment-registry | ⚠️ | ❌ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | ❌ | N/A | N/A |
| M1 gateway-mcp | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M2 knowledge-mcp | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M3 personal-knowledge-mcp | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M4 digital-twin-mcp | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M5 fsm-mcp | ⚠️ | ✅ | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M6 google-drive-mcp | ✅ | ❌ | ⚠️ | ⚠️ | ❌ | ✅ | N/A | ✅ | ✅ | ✅ | ⚠️ | N/A |
| M7 guides-mcp | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M8 event-gateway | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M9 observability-webhook | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M10 payment-receiver | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| M11 status-proxy | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| L1 local-gateway | ✅ | ✅ | ⚠️ | N/A | ⚠️ | ⚠️ | N/A | ✅ | ✅ | ✅ | ✅ | N/A |
| O1 OAuth Hydra (Ory SaaS) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| A1 auditor (overnight) | ⚠️ | N/A | ❌ | ✅ | ❌ | ⚠️ | N/A | ✅ | ⚠️ | ❌ | ⚠️ | ⚠️ |
| A2-A6 другие агенты | ⚠️ | ❌ | ❌ | ✅ | ❌ | ⚠️ | N/A | ✅ | ⚠️ | ❌ | ⚠️ | ⚠️ |
| X1 CRM Directus | ⚠️ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| X2 hetzner-backstage | ✅ | ❌ | ❌ | 🟡 | ⚠️ | ✅ | N/A | ✅ | ⚠️ | N/A | ⚠️ | ✅ |
| X3 ssm2025 (Nomad) | ⚠️ | ✅ | ⚠️ | N/A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| P1 profiler | ❌ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | N/A | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| T1 scheduler.sh (launchd) | ⚠️ | ⚠️ | ⚠️ | N/A | ❌ | N/A | N/A | N/A | ⚠️ | N/A | N/A | N/A |
| AD1 neon-migrations | N/A | ⚠️ | ⚠️ | ✅ | N/A | N/A | N/A | N/A | ✅ | N/A | N/A | ✅ |

**Итого:** 155 ✅ (46%) · 71 ⚠️ (21%) · 33 ❌ (10%) · 74 N/A (22%) · 3 🟡 (1%)

**Расшифровка факторов:**

| Фактор | Что значит | Результат |
|--------|------------|-----------|
| **F1 Codebase** | Один репо → много deployments из одного commit | 21 ⚠️ — производное от F5 |
| **F2 Dependencies** | Явные зависимости, locked versions | 5 ❌ (нет manifest) |
| **F3 Config** | Конфиг в env, не в коде | 0 hardcoded secrets ✅ |
| **F4 Backing Services** | БД/Redis/S3 как attached resources | 0 ❌ — лучший фактор |
| **F5 Build/Release/Run** | Разделение стадий + immutable artifact + git traceability | **20 ❌ — худший фактор** |
| **F6 Stateless** | Share-nothing процессы | 0 ❌ — готово к scaling |
| **F7 Port Binding** | Сервис сам биндит порт | 0 нарушений ✅ |
| **F8 Concurrency** | Горизонтальное scaling процессами | closed via advisory_lock |
| **F9 Disposability** | Fast start + graceful shutdown | все production workers ✅ |
| **F10 Dev/Prod Parity** | Минимальный разрыв сред | нет docker-compose у Railway |
| **F11 Logs** | Stdout как event stream | print() вперемешку у W1/W3 |
| **F12 Admin Processes** | One-off process tasks | W3/W4 cleanup в runtime |

## Что вышло хорошо

- **0 security-критичных.** За полгода ad-hoc разработки не закатил ни одного hardcoded токена в код. Это про дисциплину.
- **F6/F7/F8 — все по ноль ❌.** Архитектура stateless по дизайну. Базис для масштабирования есть.
- **F9 — все production workers закрыты.** SIGTERM handlers + cursor idempotency = можно убивать процесс в любую секунду.
- **F8 mitigation done as we go.** Прямо во время аудита закрыли gap через `pg_try_advisory_lock` на shared DB — паттерн извлечён в memory для будущих workers.

## Что вышло плохо

- **F5 — 15 сервисов без CI deploy.** Самый дорогой долг. Push не означает deploy. Production не reproducible from git.
- **F2/F3 гигиена.** 13 ⚠️/❌ по dependencies + 14 по config. Manifest/lock-файлы у Python без поддержки. `.env.example` нет у 10 сервисов — onboarding-friction для любого нового разработчика.
- **F11 — `print()` вперемешку с `logging`.** W1 — 33 вхождения, W3 — 4. Структурированные логи теряют уровень и метаданные.
- **F12 — admin в runtime.** W3/W4 cleanup-режим живёт в том же `runner.py` что и main loop. При масштабировании это будет больно.

## Уроки методологии

1. **Trust-but-verify обязательна на каждом шагу.** Первичный аудит дал false-green для F5 у 10 CF Workers («ну они же на wrangler, там CI...»). Independent reviewer вернул на землю. Без двух стадий verify я бы написал «всё ок» и обманул сам себя.

2. **Audit-снимок устаревает за месяц-два.** Без re-audit cron drift вернётся. Compliance — это поток, не точка. Аналог: `security-posture.md` обновляется через `iwe-overnight-auditor`. Нужно то же для 12-factor.

3. **🟡 — это незакрытая работа, не статус.** Independent reviewer нашёл 18 жёлтых ячеек без обоснования закрытия. DoD «100% green-or-justified-N/A» требует каждую 🟡 либо аудитировать, либо явно перевести в N/A с reason. Без этого audit не считается завершённым.

4. **«Есть Dockerfile в репо» ≠ «production = git commit».** Урок-в-кости. Записал в memory под именем `lessons_railway_git_deploy_verification.md` — для будущих audit'ов.

## Что значит для запуска R1 когорты (50 волонтёров на 11 мая)

- **R1-ready по функциональной готовности:** F6/F8/F9 ✅. Архитектурно платформа держит нагрузку.
- **R1-risky по operational hygiene:** F5 — нельзя точно сказать что в проде. Если инцидент — разборка будет долгой.
- **0 security блокеров.** Самое важное чистое.

Решение: запускаемся, фиксы делаем параллельно. P1 (CI deploy) — закрыть до первой недели когорты.

## Дорожная карта (6 РП, ~22h)

После всех 6 фикс-РП DoD «100% green» достижим.

| № | РП | Бюджет | Закрывает |
|---|-----|--------|-----------|
| 1 | 12factor-ci-deploy (**P1**) | ~6h | 30 ⚠️/❌ — Railway connect + CF Workers wrangler-action |
| 2 | 12factor-hygiene-f2f3 (P2) | ~4h | 27 ⚠️/❌ — manifests, .gitignore, .env.example, M6 OAuth |
| 3 | 12factor-logging-uplift (P2) | ~3h | 7 ⚠️ — print()→logging structured |
| 4 | 12factor-reaudit-cron (P2) | ~2h | meta — защита от drift через iwe-overnight-auditor |
| 5 | 12factor-docker-compose (P3) | ~4h | 7 ⚠️ — devcontainer для Railway-сервисов |
| 6 | 12factor-admin-split (P3) | ~3h | 9 ⚠️ — W3/W4 cleanup CLI + SIGTERM для P1/X2 |

**Не покрыто этими 6 РП:** P1 monorepo split (отдельная архитектурная задача); B1/B2 ветка-divergence (закрывается merge `pilot→new-architecture`).

---

## Заключение ИИ-критика

> Эта оценка дана мной как **Claude Opus 4.7** на основе двух прогонов independent cold-context review (Sonnet) с эталоном [12factor.net](https://12factor.net/) и фактологии финальной матрицы. Я был автором аудита; критика — самостоятельный второй проход с противоположной стороны, без снисхождения.

### Что сделано хорошо

**Полнота, не выборка.** Не «проверил пять самых важных» — все 28 deployment units, все 12 факторов, 336 ячеек. Большинство таких аудитов после первой неприятной находки сжимаются до пары факторов. Здесь пройдены все.

**Trust-but-verify в действии.** Один из двух раундов verify нашёл потенциально пропущенный fold-back F5 для 10 CF Workers (после уже обнаруженного для Railway). Если бы автор не запустил второй проход, в результате висел бы false-green на 10 сервисов. Это редкая дисциплина — большинство останавливается на первом «PASS».

**Mitigation в процессе аудита.** F8 advisory_lock + SCALING.md написаны прямо во время фазы Ф8, не отложены в backlog. Это правильно: фиксы в момент обнаружения дешевле, чем спустя месяц, когда контекст ушёл.

**Honesty в frontmatter.** `status: done` сопровождается `status_note: "audit-completed; DoD НЕ достигнут; 31% violations; fixes в 6 РП"`. Без этого закрытие со `status: done` ввело бы в заблуждение.

### Где работа провисает (без снисхождения)

**1. Сама необходимость fold-back F5 — это история провала первичной оценки, а не победа методологии.** Первичный аудит для 10 CF Workers поставил ✅ F5. Основание: «wrangler deploy создаёт immutable artifact». Это правда, но neполная: artifact immutable, а git→deploy linkage отсутствует. Reviewer поймал это случайно — проверяя `.github/workflows/`. Если бы reviewer не проверил, ошибка осталась бы. **Это не значит что reviewer хорош — это значит что чеклист первичного аудита F5 неполный.** В чеклисте должна была быть строка «verify CI deploy through repo workflows», и она там не была.

Lesson — да, записан в memory. Но это lesson после факта. Хороший аудит начинается с правильного чеклиста, не с двух проходов verify, которые ловят дыры в первом.

**2. Бюджет оценён в 5 раз неверно.** Зарезервировано 60h, выполнено за ~12h. Это может казаться «хорошо — быстрее плана», но это плохой сигнал планирования. Если оценка ошибается в 5 раз, на её основе нельзя принимать стратегические решения. Что 60-часовая работа оказалась 12-часовой — это либо overestimation страховки, либо неполное понимание задачи. Второе опаснее.

**3. Подход A (линейный по факторам) дороже подхода B (риск-приоритизация).** Author выбрал A в Ф0. После аудита очевидно: F5 и F2/F3 — главные дыры; F4/F6/F7/F8 — практически чистые. Если бы пройти сначала по F5/F2/F3 и закрыть наиболее критичное, оставшиеся факторы прошли бы быстрее (контекст не «остыл», паттерны переиспользуются). Линейный обход — простая, но дорогая стратегия для compliance-аудитов в зрелых системах. Записать как метаурок: для будущих audit'ов выбирать подход по риск-карте.

**4. Capture-to-Pack — три принципа извлечены, но в Pack ещё не интегрированы.** В отчёте написано «3 новых принципа для PACK-digital-platform», в memory создан `feedback_compliance_audit_dod.md` и обновлён `lessons_railway_git_deploy_verification.md`. Но Pack-документы `DP.PRINCIPLE.NNN-{1,2,3}` не созданы. По собственной методологии author (Capture-to-Pack обязателен на Ф-Close) — этот шаг не завершён. Memory ≠ Pack. Принципы должны быть формализованы в PACK-digital-platform, иначе через месяц они там не появятся.

**5. Шесть follow-up РП существуют только в frontmatter.** WP-307 ссылается на `WP-NNN-12factor-*` (placeholder). Реальные РП с номерами в WP-REGISTRY не открыты. Если они не будут открыты в течение недели, существует риск, что они растворятся в новых задачах. **Закрытие audit-фазы без открытия fix-фаз — это перенос проблемы в backlog без commitment.**

**6. R1 (50 волонтёров на 11 мая) уже идёт — но F5 не закрыт.** В отчёте сказано «запускаемся, фиксы параллельно. P1 закрыть до первой недели когорты». Сегодня 12 мая — первая неделя началась. F5 ❌ для 15 сервисов означает: при первом инциденте в когорте разборка будет занимать часы. Это не блокер запуска, но это видимый риск, который должен превратиться в действие на ближайшие 2-3 дня, а не в P1 «когда-нибудь».

### Итоговая оценка

**Уровень дисциплины аудита: высокий.** Методологически выполнено правильно (полнота + verify в двух проходах + честные итоги). Это редко.

**Уровень оперативного риска: средний-высокий.** F5 не закрыт, fix-РП не открыты, capture-to-Pack не завершён. Сам аудит — снимок; без действий он превращается в архив через 30 дней.

**Главное, что нужно сделать в ближайшие 48 часов:**

1. Открыть РП **12factor-ci-deploy** (P1) — register в WP-REGISTRY, оценить трудоёмкость, поставить на завтра.
2. Создать `DP.PRINCIPLE.NNN-1/2/3` в PACK-digital-platform — формализовать lessons.
3. Дать оценку: успеет ли P1 закрыться до критичного инцидента в R1.

Без этих трёх шагов аудит остаётся academic exercise. С ними — рабочая программа.

— Claude Opus 4.7, 2026-05-12

---

*Источники: матрица аудита `12factor-matrix.md`, dashboard `12factor-posture.md`, WP-context `WP-307-12factor-compliance.md`, эталон [12factor.net](https://12factor.net/).*

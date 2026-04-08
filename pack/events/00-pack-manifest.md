# Pack Manifest: Организация мероприятий

## Идентификатор

- **Pack ID**: `EV`
- **Версия**: 0.1.0
- **Статус**: Draft

## Область

**Название**: Организация мероприятий (Event Management)

**Описание**: Предметная область, покрывающая полный цикл создания и проведения мероприятий — от концепции до пост-событийного анализа. Применимо к образовательным, деловым, нетворкинговым, культурным и гибридным форматам.

## Scope

### В scope

- Типы и форматы мероприятий
- Проектирование концепции и программы
- Логистика и операции
- Работа с участниками, спонсорами, командой
- Управление бюджетом и рисками
- Продвижение и коммуникации
- Онлайн, офлайн и гибридные форматы
- Пост-событийный анализ и метрики

### Вне scope

- Маркетинговая стратегия компании (это PACK-ecosystem / PACK-MIM)
- Разработка учебных программ (это PACK-education)
- ИТ-платформа для регистрации/стриминга (это PACK-digital-platform)
- Управление сообществом вне мероприятий

## Entity Index

| ID | Name | Kind | Summary | Status |
|----|------|------|---------|--------|
| EV.BC.001 | Bounded Context: Организация мероприятий | BC | — | draft |
| EV.D.001 | Мероприятие ≠ Встреча ≠ Конференция | D | Различие по масштабу, цели и структуре | active |
| EV.D.002 | Концепция ≠ Программа ≠ Расписание | D | Различие по уровню детализации | active |
| EV.D.003 | Онлайн ≠ Офлайн ≠ Гибрид | D | Различие по формату присутствия | active |
| EV.D.004 | Организатор ≠ Куратор ≠ Фасилитатор | D | Различие по ролевой функции | active |
| EV.D.005 | Спонсор ≠ Партнёр ≠ Инвестор | D | Различие по типу вклада и ожиданиям | active |
| EV.ROLE.001 | Роли мероприятия | ROLE | Полная ролевая модель event-команды | active |
| EV.M.001 | Разработка концепции мероприятия | M | Event Concept Design | active |
| EV.M.002 | Программный дизайн | M | Program Design | active |
| EV.M.003 | Выбор и подготовка площадки | M | Venue Selection & Setup | active |
| EV.M.004 | Управление регистрацией и участниками | M | Registration & Attendee Management | active |
| EV.M.005 | Работа со спонсорами и партнёрами | M | Sponsorship & Partnership Management | active |
| EV.M.006 | Продвижение мероприятия | M | Event Marketing & Promotion | active |
| EV.M.007 | Операционная логистика | M | Operational Logistics | active |
| EV.M.008 | Фасилитация и модерация | M | Facilitation & Moderation | active |
| EV.M.009 | Управление бюджетом | M | Budget Management | active |
| EV.M.010 | Пост-событийный анализ | M | Post-Event Debrief & Analytics | active |
| EV.M.011 | Управление рисками | M | Event Risk Management | active |
| EV.M.012 | Гибридный формат и онлайн-трансляция | M | Hybrid & Live Streaming Setup | active |
| EV.WP.001 | Каталог рабочих продуктов мероприятия | WP | — | active |
| EV.FM.001 | Типичные ошибки при организации | FM | — | active |
| EV.FM.002 | Операционные сбои | FM | — | active |
| EV.SOTA.001 | Тренды event-индустрии 2025-2026 | SOTA | — | active |
| EV.SOTA.002 | Технологии для мероприятий 2025-2026 | SOTA | — | active |
| EV.MAP.001 | Pack Navigation Map | MAP | — | draft |

## Upstream dependencies

- SPF — Second Principles Framework
- FPF — First Principles Framework

## Downstream outputs

- DS-my-strategy — применение при планировании мероприятий Aisystant

## Maintainers

- @LiyaRooney

## Changelog

- 0.1.0 — Initial structure, April 2026

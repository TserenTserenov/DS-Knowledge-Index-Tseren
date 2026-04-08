---
id: EV.MAP.001
kind: MAP
name: Pack Navigation Map
scope: full-pack
created: 2026-04-08
last_updated: 2026-04-08
generated: false
---

# [EV.MAP.001] Pack Navigation Map — Организация мероприятий

---

## Статистика

| Kind | Count |
|------|-------|
| Bounded Context (BC) | 1 |
| Distinctions (D) | 5 |
| Methods (M) | 12 |
| Roles (ROLE) | 1 |
| Work Products (WP) | 1 |
| Failure Modes (FM) | 2 |
| SoTA (SOTA) | 2 |
| Maps (MAP) | 1 |
| **Total** | **25** |

---

## Distinctions

| ID | Name | Status |
|----|------|--------|
| EV.D.001 | Мероприятие ≠ Встреча ≠ Конференция | active |
| EV.D.002 | Концепция ≠ Программа ≠ Расписание | active |
| EV.D.003 | Онлайн ≠ Офлайн ≠ Гибрид | active |
| EV.D.004 | Организатор ≠ Куратор ≠ Фасилитатор | active |
| EV.D.005 | Спонсор ≠ Партнёр ≠ Инвестор | active |

## Roles

| ID | Name | Status |
|----|------|--------|
| EV.ROLE.001 | Роли мероприятия | active |

## Methods

| ID | Name | Status |
|----|------|--------|
| EV.M.001 | Разработка концепции мероприятия | active |
| EV.M.002 | Программный дизайн | active |
| EV.M.003 | Выбор и подготовка площадки | active |
| EV.M.004 | Управление регистрацией и участниками | active |
| EV.M.005 | Работа со спонсорами и партнёрами | active |
| EV.M.006 | Продвижение мероприятия | active |
| EV.M.007 | Операционная логистика | active |
| EV.M.008 | Фасилитация и модерация | active |
| EV.M.009 | Управление бюджетом | active |
| EV.M.010 | Пост-событийный анализ | active |
| EV.M.011 | Управление рисками | active |
| EV.M.012 | Гибридный формат и онлайн-трансляция | active |

## Work Products

| ID | Name | Status |
|----|------|--------|
| EV.WP.001 | Каталог рабочих продуктов мероприятия | active |

## Failure Modes

| ID | Name | Status |
|----|------|--------|
| EV.FM.001 | Типичные ошибки при организации | active |
| EV.FM.002 | Операционные сбои | active |

## SoTA

| ID | Name | Status |
|----|------|--------|
| EV.SOTA.001 | Тренды event-индустрии 2025-2026 | active |
| EV.SOTA.002 | Технологии для мероприятий 2025-2026 | active |

---

## Связи между методами

```
EV.M.001 Концепция
    └→ EV.M.002 Программный дизайн
         └→ EV.M.008 Фасилитация
         └→ EV.M.007 Логистика
              └→ EV.M.011 Риски
    └→ EV.M.003 Площадка
    └→ EV.M.005 Спонсоры
    └→ EV.M.006 Продвижение
         └→ EV.M.004 Регистрация
    └→ EV.M.009 Бюджет
         └→ EV.M.010 Пост-анализ
    └→ EV.M.012 Гибридный формат
```

---

*Pack EV v0.1.0 — April 2026*

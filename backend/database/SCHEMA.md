# Схема БД (3NF)

Все модели SQLAlchemy — в одном файле: `backend/app/core/models.py`  
SQL-скрипт создания таблиц: `database/init.sql`  
ER-диаграмма: `database/ER.md`

## Нормализация до 3NF

| Было (нарушение) | Стало (3NF) |
|------------------|-------------|
| `users.role` строкой | Справочник `roles` + `users.role_id` |
| ФИО одной строкой | `surname`, `name`, `patronymic` |
| Адрес пункта выдачи в заказе | Справочник `pick_up_points` + `orders.pick_up_point_id` |
| Товары внутри заказа | Таблица `product_in_order` (M:N + `amount`) |

## Таблицы

```
roles ──< users
categories ──< products >── producers
providers ──< products >── units
pick_up_points ──< orders >── order_statuses
users ──< orders ──< product_in_order >── products
```

## Справочники

- `roles` — client, manager, admin (гость только в приложении)
- `categories`, `producers`, `providers`, `units`, `order_statuses`, `pick_up_points`

## Сущности

- `users`, `products`, `orders`, `product_in_order`

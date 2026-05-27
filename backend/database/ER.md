# ER-модель базы данных (экзамен, 3NF)

> Роль **«Гость»** не хранится в БД — только в приложении (без входа).

```mermaid
erDiagram
    roles ||--o{ users : "role_id"
    categories ||--o{ products : "category_id"
    producers ||--o{ products : "producer_id"
    providers ||--o{ products : "provider_id"
    units ||--o{ products : "unit_id"
    users ||--o{ orders : "user_id"
    order_statuses ||--o{ orders : "status_id"
    pick_up_points ||--o{ orders : "pick_up_point_id"
    orders ||--o{ product_in_order : "order_id"
    products ||--o{ product_in_order : "product_id"

    roles {
        int id PK
        string code UK
        string name
    }

    users {
        int id PK
        string surname
        string name
        string patronymic
        string login UK
        string hashed_password
        int role_id FK
    }

    categories {
        int id PK
        string name UK
    }

    producers {
        int id PK
        string name UK
    }

    providers {
        int id PK
        string name UK
    }

    units {
        int id PK
        string name UK
    }

    products {
        int id PK
        string article UK
        string name
        int unit_id FK
        float price
        int provider_id FK
        int producer_id FK
        int category_id FK
        float discount
        float amount_in_stock
        text description
        string photo
    }

    order_statuses {
        int id PK
        string name UK
    }

    pick_up_points {
        int id PK
        string post_code
        string city
        string street
        string building
    }

    orders {
        int id PK
        string article
        date creation_date
        date delivery_date
        int pick_up_point_id FK
        int user_id FK
        int reception_code
        int status_id FK
    }

    product_in_order {
        int id PK
        int order_id FK
        int product_id FK
        int amount
    }
```

## Связи

| Связь | Тип | Пояснение |
|-------|-----|-----------|
| roles → users | 1:N | У пользователя одна роль |
| categories → products | 1:N | Товар в одной категории |
| producers → products | 1:N | У товара один производитель |
| providers → products | 1:N | У товара один поставщик |
| units → products | 1:N | У товара одна ед. измерения |
| users → orders | 1:N | Заказ оформляет пользователь |
| order_statuses → orders | 1:N | У заказа один статус |
| pick_up_points → orders | 1:N | Пункт выдачи для заказа |
| orders ↔ products | M:N | Через **product_in_order** (количество в `amount`) |

-- Схема БД по ER-диаграмме экзамена (3NF)
-- Модели SQLAlchemy: backend/app/core/models.py

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(25) NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50) NOT NULL DEFAULT '',
    login VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE producers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units(id),
    price REAL NOT NULL CHECK (price >= 0),
    provider_id INTEGER NOT NULL REFERENCES providers(id),
    producer_id INTEGER NOT NULL REFERENCES producers(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    discount REAL DEFAULT 0 CHECK (discount >= 0 AND discount <= 100),
    amount_in_stock REAL DEFAULT 0 CHECK (amount_in_stock >= 0),
    description TEXT,
    photo VARCHAR(500)
);

CREATE TABLE order_statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE pick_up_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_code VARCHAR(6) NOT NULL,
    city VARCHAR(30) NOT NULL,
    street VARCHAR(30) NOT NULL,
    building VARCHAR(6) NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article VARCHAR(10) NOT NULL,
    creation_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    pick_up_point_id INTEGER NOT NULL REFERENCES pick_up_points(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    reception_code INTEGER NOT NULL,
    status_id INTEGER NOT NULL REFERENCES order_statuses(id)
);

CREATE TABLE product_in_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    amount INTEGER NOT NULL CHECK (amount >= 1)
);

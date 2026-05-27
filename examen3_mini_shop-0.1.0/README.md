# Mini Shop

Мини интернет-магазин на **Vue 3 + FastAPI + SQLAlchemy + SQLite**.

В pip-пакет входят **исходники Vue** (`.vue`, `.js`), без production-сборки — можно править на экзамене.

## Установка через pip (экзамен)

```bash
pip install examen3-mini-shop
```

### Запуск

**Терминал 1 — backend:**

```bash
mini-shop
```

**Терминал 2 — frontend (исходники Vue):**

```bash
mini-shop frontend
```

- Backend API: http://127.0.0.1:8000/docs  
- Frontend: http://localhost:5173  

**Админ:** `admin@example.com` / `admin123`

### Где лежат исходники после pip install

```bash
mini-shop frontend-path
```

Обычно это что-то вроде:

`.../site-packages/app/frontend/src/`

Там можно открыть проект в IDE и менять компоненты — `npm run dev` подхватит изменения.

Данные (БД, загрузки): `~/.mini_shop/`

## Публикация на PyPI

```bash
python scripts/build_package.py
pip install twine
twine upload dist/*
```

Проверка на TestPyPI:

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ examen3-mini-shop
```

> Имя `examen3-mini-shop` должно быть свободно на PyPI. Если занято — измените `name` в `pyproject.toml`.

## Разработка из репозитория

### Backend

```bash
pip install -e .
mini-shop --reload --port 8000
```

### Frontend

```bash
cd backend/app/frontend
npm install
npm run dev
```

## Структура

```
backend/app/
├── auth/ categories/ products/   # DDD-модули API
├── frontend/                     # исходники Vue (в pip-пакете)
│   ├── src/components/
│   ├── src/views/
│   └── package.json
├── cli.py                        # команда mini-shop
└── main.py
pyproject.toml
```

## Возможности

- Регистрация и авторизация (JWT)
- Каталог товаров с фильтром по категориям
- Карточка товара с фото
- CRUD товаров и категорий (только admin)
- Загрузка изображений товаров

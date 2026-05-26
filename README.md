# Mini Shop

Мини интернет-магазин на **Vue 3 + FastAPI + SQLAlchemy + SQLite**.

## Структура

- `backend/` — API с DDD-разбиением (domain / infra / app / api)
- `frontend/` — Vue-компоненты, views, API-клиент

## Запуск backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

API: http://127.0.0.1:8001  
Документация: http://127.0.0.1:8001/docs

### Админ по умолчанию

- Email: `admin@example.com`
- Пароль: `admin123`

## Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

Сайт: http://localhost:5173

## Возможности

- Регистрация и авторизация (JWT)
- Каталог товаров с фильтром по категориям
- Карточка товара с фото
- CRUD товаров и категорий (только admin)
- Загрузка изображений товаров

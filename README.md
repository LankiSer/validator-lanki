# Mini Shop — строительные материалы

- `backend/` — FastAPI + SQLAlchemy + SQLite  
- `frontend/` — Vue 3 + Vite  

**Поиск и фильтрация (код для печати):** [GUIDE.md](GUIDE.md)

## Запуск

**Backend:**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

- API: http://127.0.0.1:8000/docs  
- Сайт: http://localhost:5173  

После смены моделей удалите БД:

```powershell
Remove-Item "$env:USERPROFILE\.mini_shop\shop.db" -ErrorAction SilentlyContinue
```

## Пользователи

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | admin | admin123 |
| Менеджер | manager | manager123 |
| Клиент | client | client123 |
| Гость | кнопка на экране входа | — |

## База данных

| Файл | Описание |
|------|----------|
| `backend/app/core/models.py` | Модели SQLAlchemy |
| `backend/database/init.sql` | SQL таблиц |
| `backend/database/ER.md` | ER-диаграмма |
| `backend/database/SCHEMA.md` | 3NF |

БД: `%USERPROFILE%\.mini_shop\shop.db` (создаётся при старте backend).

API: префикс `/api`.

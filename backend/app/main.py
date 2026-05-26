from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.api.router import router as auth_router
from app.auth.infra.models import UserModel
from app.categories.api.router import router as categories_router
from app.categories.infra.models import CategoryModel
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.products.api.router import router as products_router
from app.products.infra.models import ProductModel

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_path = Path(settings.upload_dir)
upload_path.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_path)), name="uploads")


def seed_data() -> None:
    db = SessionLocal()
    try:
        if db.query(UserModel).count() == 0:
            admin = UserModel(
                email="admin@example.com",
                username="admin",
                hashed_password=hash_password("admin123"),
                is_admin=True,
            )
            db.add(admin)

        if db.query(CategoryModel).count() == 0:
            categories = [
                CategoryModel(name="Электроника", slug="elektronika"),
                CategoryModel(name="Одежда", slug="odezhda"),
                CategoryModel(name="Книги", slug="knigi"),
            ]
            db.add_all(categories)
            db.commit()

            products = [
                ProductModel(
                    name="Наушники",
                    description="Беспроводные наушники с шумоподавлением",
                    price=4990,
                    stock=15,
                    category_id=1,
                ),
                ProductModel(
                    name="Футболка",
                    description="Хлопковая футболка, размер M",
                    price=1290,
                    stock=30,
                    category_id=2,
                ),
                ProductModel(
                    name="Python для начинающих",
                    description="Учебник по программированию",
                    price=890,
                    stock=20,
                    category_id=3,
                ),
            ]
            db.add_all(products)

        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    seed_data()


app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)


@app.get("/health")
def health():
    return {"status": "ok"}

from datetime import date, timedelta
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.auth.api.router import router as auth_router
from app.categories.api.router import router as categories_router
from app.core.config import ensure_data_dirs, settings
from app.core.database import Base, SessionLocal, engine
from app.core.models import (
    CategoryModel,
    OrderModel,
    OrderStatusModel,
    PickUpPointModel,
    ProducerModel,
    ProductInOrderModel,
    ProductModel,
    ProviderModel,
    RoleModel,
    UnitModel,
    UserModel,
)
from app.core.security import hash_password
from app.manufacturers.api.router import router as producers_router
from app.orders.api.router import router as orders_router
from app.products.api.router import router as products_router
from app.shared.roles import ADMIN, CLIENT, MANAGER

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_path = Path(settings.upload_dir)
upload_path.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_path)), name="uploads")

assets_path = Path(__file__).resolve().parent / "assets"
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")


@app.get("/picture.png", include_in_schema=False)
def placeholder_image():
    picture = assets_path / "picture.png"
    if picture.exists():
        return FileResponse(picture)
    return FileResponse(picture, status_code=404)


def seed_data() -> None:
    db = SessionLocal()
    try:
        if db.query(RoleModel).count() == 0:
            db.add_all(
                [
                    RoleModel(code=ADMIN, name="Администратор"),
                    RoleModel(code=MANAGER, name="Менеджер"),
                    RoleModel(code=CLIENT, name="Клиент"),
                ]
            )
            db.commit()

        if db.query(UserModel).count() == 0:
            roles = {r.code: r.id for r in db.query(RoleModel).all()}
            db.add_all(
                [
                    UserModel(
                        surname="Иванов",
                        name="Иван",
                        patronymic="Иванович",
                        login="admin",
                        hashed_password=hash_password("admin123"),
                        role_id=roles[ADMIN],
                    ),
                    UserModel(
                        surname="Петров",
                        name="Пётр",
                        patronymic="Петрович",
                        login="manager",
                        hashed_password=hash_password("manager123"),
                        role_id=roles[MANAGER],
                    ),
                    UserModel(
                        surname="Сидоров",
                        name="Сидор",
                        patronymic="Сидорович",
                        login="client",
                        hashed_password=hash_password("client123"),
                        role_id=roles[CLIENT],
                    ),
                ]
            )

        if db.query(ProducerModel).count() == 0:
            db.add_all(
                [
                    ProducerModel(name="Knauf"),
                    ProducerModel(name="Ceresit"),
                    ProducerModel(name="Rockwool"),
                ]
            )

        if db.query(ProviderModel).count() == 0:
            db.add_all(
                [
                    ProviderModel(name="СтройОпт"),
                    ProviderModel(name="КерамПром"),
                    ProviderModel(name="ТеплоДом"),
                ]
            )

        if db.query(UnitModel).count() == 0:
            db.add_all(
                [
                    UnitModel(name="меш."),
                    UnitModel(name="шт."),
                    UnitModel(name="уп."),
                ]
            )

        if db.query(CategoryModel).count() == 0:
            db.add_all(
                [
                    CategoryModel(name="Цемент и смеси"),
                    CategoryModel(name="Кирпич"),
                    CategoryModel(name="Утеплители"),
                ]
            )
            db.commit()

        if db.query(PickUpPointModel).count() == 0:
            db.add(
                PickUpPointModel(
                    post_code="123456",
                    city="Москва",
                    street="ул. Строителей",
                    building="15",
                )
            )
            db.commit()

        if db.query(OrderStatusModel).count() == 0:
            db.add_all(
                [
                    OrderStatusModel(name="Новый"),
                    OrderStatusModel(name="В обработке"),
                    OrderStatusModel(name="Доставлен"),
                    OrderStatusModel(name="Отменён"),
                ]
            )

        if db.query(ProductModel).count() == 0:
            db.add_all(
                [
                    ProductModel(
                        article="A000000001",
                        name="Цемент М500",
                        description="Портландцемент",
                        category_id=1,
                        producer_id=1,
                        provider_id=1,
                        unit_id=1,
                        price=420.50,
                        amount_in_stock=120,
                        discount=5,
                    ),
                    ProductModel(
                        article="A000000002",
                        name="Кирпич керамический",
                        description="Полнотелый кирпич М-150",
                        category_id=2,
                        producer_id=2,
                        provider_id=2,
                        unit_id=2,
                        price=18.90,
                        amount_in_stock=5000,
                        discount=0,
                    ),
                    ProductModel(
                        article="A000000003",
                        name="Плита минеральная",
                        description="Теплоизоляция фасада",
                        category_id=3,
                        producer_id=3,
                        provider_id=3,
                        unit_id=3,
                        price=650.00,
                        amount_in_stock=80,
                        discount=10,
                    ),
                ]
            )
            db.commit()

        if db.query(OrderModel).count() == 0:
            admin_id = db.query(UserModel).filter(UserModel.login == "admin").first().id
            order = OrderModel(
                article="ORD0000001",
                user_id=admin_id,
                pick_up_point_id=1,
                reception_code=123456,
                status_id=1,
                creation_date=date.today(),
                delivery_date=date.today() + timedelta(days=3),
            )
            db.add(order)
            db.flush()
            db.add(ProductInOrderModel(order_id=order.id, product_id=1, amount=2))

        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    ensure_data_dirs()
    Base.metadata.create_all(bind=engine)
    seed_data()


api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(producers_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)
app.include_router(api_router)


@app.get("/health")
def health():
    from app import __version__

    return {"status": "ok", "version": __version__}

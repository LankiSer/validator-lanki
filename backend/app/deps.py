from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.app.service import AuthService
from app.auth.domain.entity import UserEntity
from app.auth.infra.repository import UserRepository
from app.categories.app.service import CategoryService
from app.categories.infra.repository import CategoryRepository
from app.core.database import get_db
from app.core.security import decode_access_token
from app.manufacturers.app.service import ManufacturerService
from app.manufacturers.infra.repository import ManufacturerRepository
from app.orders.app.service import OrderService
from app.orders.infra.repository import OrderRepository
from app.products.app.service import ProductService
from app.products.infra.refs_repository import RefsRepository
from app.products.infra.repository import ProductRepository
from app.shared.roles import ADMIN, MANAGER, can_manage_orders, can_manage_products, can_view_orders

security = HTTPBearer(auto_error=False)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def get_manufacturer_service(db: Session = Depends(get_db)) -> ManufacturerService:
    return ManufacturerService(ManufacturerRepository(db))


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db), RefsRepository(db))


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(
        ProductRepository(db),
        CategoryRepository(db),
        ManufacturerRepository(db),
        OrderRepository(db),
        RefsRepository(db),
    )


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> UserEntity | None:
    if not credentials:
        return None
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        return None
    return UserRepository(db).get_by_id(int(user_id))


def get_current_user(user: UserEntity | None = Depends(get_optional_user)) -> UserEntity:
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Требуется авторизация")
    return user


def require_admin(user: UserEntity = Depends(get_current_user)) -> UserEntity:
    if not can_manage_products(user.role):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ только для администратора")
    return user


def require_manager(user: UserEntity = Depends(get_current_user)) -> UserEntity:
    if not can_view_orders(user.role):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Раздел заказов доступен менеджеру и администратору",
        )
    return user

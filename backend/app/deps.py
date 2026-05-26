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
from app.products.app.service import ProductService
from app.products.infra.repository import ProductRepository

security = HTTPBearer(auto_error=False)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db), CategoryRepository(db))


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> UserEntity:
    if not credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Требуется авторизация")

    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Недействительный токен")

    user = UserRepository(db).get_by_id(int(user_id))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Пользователь не найден")
    return user


def require_admin(user: UserEntity = Depends(get_current_user)) -> UserEntity:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ только для администратора")
    return user

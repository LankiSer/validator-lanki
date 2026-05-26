from fastapi import HTTPException, status

from app.auth.app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.auth.infra.repository import UserRepository
from app.core.security import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def register(self, data: RegisterRequest) -> TokenResponse:
        if self._repo.get_by_email(data.email):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email уже занят")
        if self._repo.get_by_username(data.username):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Имя пользователя занято")

        user = self._repo.create(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        return self._build_token(user)

    def login(self, data: LoginRequest) -> TokenResponse:
        stored_hash = self._repo.get_password_hash(data.email)
        if not stored_hash or not verify_password(data.password, stored_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный email или пароль")

        user = self._repo.get_by_email(data.email)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Пользователь не найден")
        return self._build_token(user)

    def get_profile(self, user_id: int) -> UserResponse:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
        return UserResponse(**user.__dict__)

    def _build_token(self, user) -> TokenResponse:
        token = create_access_token(str(user.id))
        return TokenResponse(
            access_token=token,
            user=UserResponse(**user.__dict__),
        )

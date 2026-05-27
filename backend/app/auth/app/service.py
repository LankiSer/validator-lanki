from fastapi import HTTPException, status

from app.auth.app.schemas import LoginRequest, TokenResponse, UserResponse
from app.auth.infra.repository import UserRepository
from app.core.security import create_access_token, verify_password


class AuthService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def login(self, data: LoginRequest) -> TokenResponse:
        stored_hash = self._repo.get_password_hash(data.login)
        if not stored_hash or not verify_password(data.password, stored_hash):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Неверный логин или пароль. Проверьте данные и повторите вход.",
            )

        user = self._repo.get_by_login(data.login)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Пользователь не найден")
        return self._build_token(user)

    def get_profile(self, user_id: int) -> UserResponse:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
        return self._to_response(user)

    def _build_token(self, user) -> TokenResponse:
        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token, user=self._to_response(user))

    def _to_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id,
            surname=user.surname,
            name=user.name,
            patronymic=user.patronymic,
            login=user.login,
            role=user.role,
            full_name=user.full_name,
        )

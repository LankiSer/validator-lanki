from sqlalchemy.orm import Session, joinedload

from app.auth.domain.entity import UserEntity
from app.core.models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def _base_query(self):
        return self._db.query(UserModel).options(joinedload(UserModel.role))

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            surname=model.surname,
            name=model.name,
            patronymic=model.patronymic or "",
            login=model.login,
            role=model.role.code,
        )

    def get_by_login(self, login: str) -> UserEntity | None:
        model = self._base_query().filter(UserModel.login == login).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: int) -> UserEntity | None:
        model = self._base_query().filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def get_password_hash(self, login: str) -> str | None:
        model = self._db.query(UserModel).filter(UserModel.login == login).first()
        return model.hashed_password if model else None

from sqlalchemy.orm import Session

from app.auth.domain.entity import UserEntity
from app.auth.infra.models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            username=model.username,
            is_admin=model.is_admin,
        )

    def get_by_email(self, email: str) -> UserEntity | None:
        model = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def get_by_username(self, username: str) -> UserEntity | None:
        model = self._db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: int) -> UserEntity | None:
        model = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def get_password_hash(self, email: str) -> str | None:
        model = self._db.query(UserModel).filter(UserModel.email == email).first()
        return model.hashed_password if model else None

    def create(self, email: str, username: str, hashed_password: str) -> UserEntity:
        model = UserModel(
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_admin=False,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

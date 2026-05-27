from sqlalchemy.orm import Session

from app.categories.domain.entity import CategoryEntity
from app.core.models import CategoryModel


class CategoryRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_entity(self, model: CategoryModel) -> CategoryEntity:
        return CategoryEntity(id=model.id, name=model.name)

    def list_all(self) -> list[CategoryEntity]:
        models = self._db.query(CategoryModel).order_by(CategoryModel.name).all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, category_id: int) -> CategoryEntity | None:
        model = self._db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        return self._to_entity(model) if model else None

    def create(self, name: str) -> CategoryEntity:
        model = CategoryModel(name=name)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, category_id: int, name: str) -> CategoryEntity | None:
        model = self._db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not model:
            return None
        model.name = name
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def delete(self, category_id: int) -> bool:
        model = self._db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not model:
            return False
        self._db.delete(model)
        self._db.commit()
        return True

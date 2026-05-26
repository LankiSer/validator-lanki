from sqlalchemy.orm import Session

from app.products.domain.entity import ProductEntity
from app.products.infra.models import ProductModel


class ProductRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_entity(self, model: ProductModel) -> ProductEntity:
        return ProductEntity(
            id=model.id,
            name=model.name,
            description=model.description or "",
            price=model.price,
            stock=model.stock,
            category_id=model.category_id,
            image_url=model.image_url,
        )

    def list_all(self, category_id: int | None = None) -> list[ProductEntity]:
        query = self._db.query(ProductModel)
        if category_id:
            query = query.filter(ProductModel.category_id == category_id)
        models = query.order_by(ProductModel.id.desc()).all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._to_entity(model) if model else None

    def create(self, data: dict) -> ProductEntity:
        model = ProductModel(**data)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, product_id: int, data: dict) -> ProductEntity | None:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(model, key, value)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def delete(self, product_id: int) -> bool:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False
        self._db.delete(model)
        self._db.commit()
        return True

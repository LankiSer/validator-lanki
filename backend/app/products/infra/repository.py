from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from app.core.models import ProductModel, ProviderModel, UnitModel
from app.products.domain.entity import ProductEntity


class ProductRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_entity(self, model: ProductModel) -> ProductEntity:
        return ProductEntity(
            id=model.id,
            article=model.article,
            name=model.name,
            category_id=model.category_id,
            category_name=model.category.name,
            producer_id=model.producer_id,
            producer_name=model.producer.name,
            provider_id=model.provider_id,
            provider_name=model.provider.name,
            unit_id=model.unit_id,
            unit_name=model.unit.name,
            price=model.price,
            amount_in_stock=model.amount_in_stock,
            discount=model.discount or 0.0,
            description=model.description or "",
            photo=model.photo,
        )

    def _base_query(self):
        return self._db.query(ProductModel).options(
            joinedload(ProductModel.category),
            joinedload(ProductModel.producer),
            joinedload(ProductModel.provider),
            joinedload(ProductModel.unit),
        )

    def list_filtered(
        self,
        search: str | None = None,
        producer_id: int | None = None,
        category_id: int | None = None,
        sort_by: str | None = None,
        sort_dir: str = "asc",
    ) -> list[ProductEntity]:
        query = self._base_query()

        if producer_id:
            query = query.filter(ProductModel.producer_id == producer_id)
        if category_id:
            query = query.filter(ProductModel.category_id == category_id)
        if search:
            pattern = f"%{search.strip()}%"
            query = (
                query.join(ProductModel.provider)
                .join(ProductModel.unit)
                .filter(
                    or_(
                        ProductModel.article.ilike(pattern),
                        ProductModel.name.ilike(pattern),
                        ProductModel.description.ilike(pattern),
                        ProviderModel.name.ilike(pattern),
                        UnitModel.name.ilike(pattern),
                    )
                )
            )

        sort_map = {
            "stock": ProductModel.amount_in_stock,
            "amount_in_stock": ProductModel.amount_in_stock,
            "price": ProductModel.price,
            "discount": ProductModel.discount,
        }
        column = sort_map.get(sort_by or "")
        if column is not None:
            direction = desc if sort_dir == "desc" else asc
            query = query.order_by(direction(column))
        else:
            query = query.order_by(ProductModel.id.asc())

        return [self._to_entity(m) for m in query.all()]

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        model = self._base_query().filter(ProductModel.id == product_id).first()
        return self._to_entity(model) if model else None

    def create(self, data: dict) -> ProductEntity:
        model = ProductModel(**data)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self.get_by_id(model.id)

    def update(self, product_id: int, data: dict) -> ProductEntity | None:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(model, key, value)
        self._db.commit()
        return self.get_by_id(product_id)

    def delete(self, product_id: int) -> bool:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False
        self._db.delete(model)
        self._db.commit()
        return True

    def get_photo_path(self, product_id: int) -> str | None:
        model = self._db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return model.photo if model else None

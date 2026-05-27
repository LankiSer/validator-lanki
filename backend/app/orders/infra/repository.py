from sqlalchemy.orm import Session, joinedload

from app.core.models import OrderModel, OrderStatusModel, ProductInOrderModel
from app.orders.domain.entity import OrderEntity, OrderLineEntity


class OrderRepository:
    def __init__(self, db: Session):
        self._db = db

    def _base_query(self):
        return self._db.query(OrderModel).options(
            joinedload(OrderModel.status),
            joinedload(OrderModel.user),
            joinedload(OrderModel.pick_up_point),
            joinedload(OrderModel.lines),
        )

    def _to_entity(self, model: OrderModel) -> OrderEntity:
        return OrderEntity(
            id=model.id,
            article=model.article,
            user_id=model.user_id,
            user_login=model.user.login,
            user_full_name=model.user.full_name,
            status_id=model.status_id,
            status_name=model.status.name,
            pick_up_point_id=model.pick_up_point_id,
            pick_up_address=model.pick_up_point.full_address,
            reception_code=model.reception_code,
            creation_date=model.creation_date,
            delivery_date=model.delivery_date,
            lines=[
                OrderLineEntity(product_id=line.product_id, amount=line.amount)
                for line in model.lines
            ],
        )

    def list_statuses(self) -> list[OrderStatusModel]:
        return self._db.query(OrderStatusModel).order_by(OrderStatusModel.id).all()

    def list_orders(self) -> list[OrderEntity]:
        models = self._base_query().order_by(OrderModel.id.desc()).all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, order_id: int) -> OrderEntity | None:
        model = self._base_query().filter(OrderModel.id == order_id).first()
        return self._to_entity(model) if model else None

    def create(self, data: dict, lines: list[dict]) -> OrderEntity:
        model = OrderModel(**data)
        self._db.add(model)
        self._db.flush()
        for line in lines:
            self._db.add(
                ProductInOrderModel(
                    order_id=model.id,
                    product_id=line["product_id"],
                    amount=line["amount"],
                )
            )
        self._db.commit()
        return self.get_by_id(model.id)

    def update(self, order_id: int, data: dict) -> OrderEntity | None:
        model = self._db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not model:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(model, key, value)
        self._db.commit()
        return self.get_by_id(order_id)

    def delete(self, order_id: int) -> bool:
        model = self._db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not model:
            return False
        self._db.delete(model)
        self._db.commit()
        return True

    def product_in_orders(self, product_id: int) -> bool:
        return (
            self._db.query(ProductInOrderModel)
            .filter(ProductInOrderModel.product_id == product_id)
            .count()
            > 0
        )

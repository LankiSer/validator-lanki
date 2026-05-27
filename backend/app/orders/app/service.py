from fastapi import HTTPException, status

from app.orders.app.schemas import (
    OrderCreate,
    OrderLineResponse,
    OrderResponse,
    OrderStatusResponse,
    OrderUpdate,
)
from app.orders.infra.repository import OrderRepository
from app.products.infra.refs_repository import RefsRepository


class OrderService:
    def __init__(self, repo: OrderRepository, refs_repo: RefsRepository):
        self._repo = repo
        self._refs_repo = refs_repo

    def list_statuses(self) -> list[OrderStatusResponse]:
        return [OrderStatusResponse(id=s.id, name=s.name) for s in self._repo.list_statuses()]

    def list_orders(self) -> list[OrderResponse]:
        return [self._to_response(o) for o in self._repo.list_orders()]

    def get_order(self, order_id: int) -> OrderResponse:
        order = self._repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
        return self._to_response(order)

    def create(self, data: OrderCreate, user_id: int) -> OrderResponse:
        if not self._refs_repo.pick_up_point_exists(data.pick_up_point_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Пункт выдачи не найден")
        payload = data.model_dump(exclude={"lines"})
        payload["user_id"] = user_id
        lines = [line.model_dump() for line in data.lines]
        order = self._repo.create(payload, lines)
        return self._to_response(order)

    def update(self, order_id: int, data: OrderUpdate) -> OrderResponse:
        payload = data.model_dump(exclude_unset=True)
        if "pick_up_point_id" in payload and not self._refs_repo.pick_up_point_exists(
            payload["pick_up_point_id"]
        ):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Пункт выдачи не найден")
        order = self._repo.update(order_id, payload)
        if not order:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
        return self._to_response(order)

    def delete(self, order_id: int) -> None:
        if not self._repo.delete(order_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")

    def _to_response(self, order) -> OrderResponse:
        return OrderResponse(
            id=order.id,
            article=order.article,
            user_id=order.user_id,
            user_login=order.user_login,
            user_full_name=order.user_full_name,
            status_id=order.status_id,
            status_name=order.status_name,
            pick_up_point_id=order.pick_up_point_id,
            pick_up_address=order.pick_up_address,
            reception_code=order.reception_code,
            creation_date=order.creation_date,
            delivery_date=order.delivery_date,
            lines=[
                OrderLineResponse(product_id=line.product_id, amount=line.amount)
                for line in order.lines
            ],
        )

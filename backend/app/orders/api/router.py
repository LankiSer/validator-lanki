from fastapi import APIRouter, Depends

from app.auth.domain.entity import UserEntity
from app.deps import get_order_service, require_admin, require_manager
from app.orders.app.schemas import OrderCreate, OrderResponse, OrderStatusResponse, OrderUpdate
from app.orders.app.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/statuses", response_model=list[OrderStatusResponse])
def list_statuses(
    _: object = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    return service.list_statuses()


@router.get("", response_model=list[OrderResponse])
def list_orders(
    _: object = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    return service.list_orders()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    _: object = Depends(require_manager),
    service: OrderService = Depends(get_order_service),
):
    return service.get_order(order_id)


@router.post("", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    user: UserEntity = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    return service.create(data, user_id=user.id)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    data: OrderUpdate,
    _: object = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    return service.update(order_id, data)


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    _: object = Depends(require_admin),
    service: OrderService = Depends(get_order_service),
):
    service.delete(order_id)

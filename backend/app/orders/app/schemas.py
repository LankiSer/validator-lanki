from datetime import date

from pydantic import BaseModel, Field


class OrderStatusResponse(BaseModel):
    id: int
    name: str


class OrderLineCreate(BaseModel):
    product_id: int
    amount: int = Field(ge=1, default=1)


class OrderLineResponse(BaseModel):
    product_id: int
    amount: int


class OrderCreate(BaseModel):
    article: str = Field(min_length=1, max_length=10)
    status_id: int
    pick_up_point_id: int
    reception_code: int
    creation_date: date
    delivery_date: date
    lines: list[OrderLineCreate] = []


class OrderUpdate(BaseModel):
    article: str | None = Field(default=None, min_length=1, max_length=10)
    status_id: int | None = None
    pick_up_point_id: int | None = None
    reception_code: int | None = None
    creation_date: date | None = None
    delivery_date: date | None = None


class OrderResponse(BaseModel):
    id: int
    article: str
    user_id: int
    user_login: str
    user_full_name: str
    status_id: int
    status_name: str
    pick_up_point_id: int
    pick_up_address: str
    reception_code: int
    creation_date: date
    delivery_date: date
    lines: list[OrderLineResponse] = []

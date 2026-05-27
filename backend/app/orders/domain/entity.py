from dataclasses import dataclass
from datetime import date


@dataclass
class OrderLineEntity:
    product_id: int
    amount: int


@dataclass
class OrderEntity:
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
    lines: list[OrderLineEntity]

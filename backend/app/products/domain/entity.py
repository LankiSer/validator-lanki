from dataclasses import dataclass


@dataclass
class ProductEntity:
    id: int
    article: str
    name: str
    category_id: int
    category_name: str
    producer_id: int
    producer_name: str
    provider_id: int
    provider_name: str
    unit_id: int
    unit_name: str
    price: float
    amount_in_stock: float
    discount: float
    description: str
    photo: str | None

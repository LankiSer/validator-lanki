from dataclasses import dataclass


@dataclass
class ProductEntity:
    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int
    image_url: str | None

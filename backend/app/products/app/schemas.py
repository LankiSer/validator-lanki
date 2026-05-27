from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    article: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    description: str = ""
    category_id: int
    producer_id: int
    provider_id: int
    unit_id: int
    price: float = Field(ge=0)
    amount_in_stock: float = Field(ge=0)
    discount: float = Field(ge=0, le=100)


class ProductUpdate(BaseModel):
    article: str | None = Field(default=None, min_length=1, max_length=10)
    name: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = None
    category_id: int | None = None
    producer_id: int | None = None
    provider_id: int | None = None
    unit_id: int | None = None
    price: float | None = Field(default=None, ge=0)
    amount_in_stock: float | None = Field(default=None, ge=0)
    discount: float | None = Field(default=None, ge=0, le=100)


class ProductResponse(BaseModel):
    id: int
    article: str
    name: str
    description: str
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
    photo: str | None


class ProviderResponse(BaseModel):
    id: int
    name: str


class UnitResponse(BaseModel):
    id: int
    name: str


class PickUpPointResponse(BaseModel):
    id: int
    post_code: str
    city: str
    street: str
    building: str
    full_address: str

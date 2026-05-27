from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str

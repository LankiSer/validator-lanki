from pydantic import BaseModel


class ManufacturerResponse(BaseModel):
    id: int
    name: str

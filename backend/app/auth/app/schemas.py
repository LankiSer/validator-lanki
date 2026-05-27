from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    login: str = Field(min_length=2, max_length=50)
    password: str


class UserResponse(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    login: str
    role: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

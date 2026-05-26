from fastapi import APIRouter, Depends

from app.auth.app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.auth.app.service import AuthService
from app.deps import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    return service.register(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(data)


@router.get("/me", response_model=UserResponse)
def me(user=Depends(get_current_user)):
    return UserResponse(**user.__dict__)

from fastapi import APIRouter, HTTPException, status

from app.auth.admin import validate_admin_token
from app.deps import AdminUser, AppSettings
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, settings: AppSettings):
    if not validate_admin_token(payload.token, settings):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return LoginResponse(access_token=payload.token, role="admin")


@router.get("/me", response_model=MeResponse)
def me(admin: AdminUser):
    return MeResponse(role=admin["role"], authenticated=True)


# Also expose under /admin/login for plan compatibility
admin_auth_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_auth_router.post("/login", response_model=LoginResponse)
def admin_login(payload: LoginRequest, settings: AppSettings):
    if not validate_admin_token(payload.token, settings):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return LoginResponse(access_token=payload.token, role="admin")

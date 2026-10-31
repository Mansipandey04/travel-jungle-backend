from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    token: str = Field(min_length=1, max_length=500)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str = "admin"


class MeResponse(BaseModel):
    role: str
    authenticated: bool

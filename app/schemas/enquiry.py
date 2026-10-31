from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EnquiryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    message: str = Field(min_length=1, max_length=5000)
    source_type: str | None = Field(default=None, max_length=64)
    source_id: int | None = None


class EnquiryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None
    message: str
    source_type: str | None
    source_id: int | None
    created_at: datetime | None = None

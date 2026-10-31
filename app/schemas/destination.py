from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DestinationBase(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=200)
    region: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=1, max_length=120)
    summary: str = Field(min_length=1, max_length=10000)
    hero_image_url: str | None = None
    editorial: dict[str, Any] | None = None
    is_published: bool = True
    is_demo: bool = False


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    region: str | None = Field(default=None, min_length=1, max_length=120)
    state: str | None = Field(default=None, min_length=1, max_length=120)
    summary: str | None = Field(default=None, min_length=1, max_length=10000)
    hero_image_url: str | None = None
    editorial: dict[str, Any] | None = None
    is_published: bool | None = None
    is_demo: bool | None = None


class DestinationOut(DestinationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

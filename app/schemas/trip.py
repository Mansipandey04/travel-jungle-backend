from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ItineraryDay


class TripBase(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    destination_id: int
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=10000)
    duration_days: int | None = Field(default=None, ge=1)
    itinerary: list[ItineraryDay] | list[dict[str, Any]] | None = None
    inclusions: list[str] | dict[str, Any] | None = None
    hero_image_url: str | None = None
    is_published: bool = True
    is_demo: bool = False


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    destination_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    summary: str | None = Field(default=None, min_length=1, max_length=10000)
    duration_days: int | None = Field(default=None, ge=1)
    itinerary: list[ItineraryDay] | list[dict[str, Any]] | None = None
    inclusions: list[str] | dict[str, Any] | None = None
    hero_image_url: str | None = None
    is_published: bool | None = None
    is_demo: bool | None = None


class TripOut(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    destination_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=10000)
    starts_on: date | None = None
    ends_on: date | None = None
    location_label: str | None = Field(default=None, max_length=200)
    hero_image_url: str | None = None
    is_published: bool = True
    is_demo: bool = False


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    destination_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    summary: str | None = Field(default=None, min_length=1, max_length=10000)
    starts_on: date | None = None
    ends_on: date | None = None
    location_label: str | None = Field(default=None, max_length=200)
    hero_image_url: str | None = None
    is_published: bool | None = None
    is_demo: bool | None = None


class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

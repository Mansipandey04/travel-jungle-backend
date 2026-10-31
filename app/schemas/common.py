from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class Page(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta


class MessageOut(BaseModel):
    message: str


def clamp_pagination(page: int = 1, page_size: int = 20) -> tuple[int, int]:
    page = max(1, page)
    page_size = min(50, max(1, page_size))
    return page, page_size


class LayerBlock(BaseModel):
    headline: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1, max_length=20000)
    tips: list[str] = Field(default_factory=list)
    media_refs: list[str] = Field(default_factory=list)


class ItineraryDay(BaseModel):
    day: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=5000)

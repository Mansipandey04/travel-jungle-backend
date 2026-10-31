from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StoryStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class StorySource(str, Enum):
    editorial = "editorial"
    community = "community"


class CommunityStoryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body_md: str = Field(min_length=1, max_length=20000)
    author_display: str = Field(min_length=1, max_length=120)
    destination_slug: str | None = Field(default=None, max_length=120)
    slug: str | None = Field(default=None, max_length=120)


class StoryModerate(BaseModel):
    status: StoryStatus


class StoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    destination_id: int | None = None
    title: str
    body_md: str
    author_display: str
    status: str
    source: str
    is_demo: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class StoryAdminCreate(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=200)
    body_md: str = Field(min_length=1, max_length=20000)
    author_display: str = Field(min_length=1, max_length=120)
    destination_id: int | None = None
    status: StoryStatus = StoryStatus.approved
    source: StorySource = StorySource.editorial
    is_demo: bool = False

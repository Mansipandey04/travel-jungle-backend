from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class StoryStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class StorySource(str, Enum):
    editorial = "editorial"
    community = "community"


class TravelStory(Base):
    __tablename__ = "travel_stories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    destination_id: Mapped[int | None] = mapped_column(ForeignKey("destinations.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    body_md: Mapped[str] = mapped_column(Text)
    author_display: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(32), default=StoryStatus.pending.value, index=True)
    source: Mapped[str] = mapped_column(String(32), default=StorySource.community.value)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    destination = relationship("Destination", back_populates="travel_stories")
    images = relationship("StoryImage", back_populates="travel_story")


class StoryImage(Base):
    __tablename__ = "story_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    travel_story_id: Mapped[int | None] = mapped_column(ForeignKey("travel_stories.id"), nullable=True, index=True)
    hidden_india_story_id: Mapped[int | None] = mapped_column(
        ForeignKey("hidden_india_stories.id"), nullable=True, index=True
    )
    url: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str] = mapped_column(String(300), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    credit: Mapped[str | None] = mapped_column(String(200), nullable=True)

    travel_story = relationship("TravelStory", back_populates="images")
    hidden_india_story = relationship("HiddenIndiaStory", back_populates="images")

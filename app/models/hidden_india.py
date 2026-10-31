from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db import Base

JSONType = JSON().with_variant(JSONB(), "postgresql")


class HiddenIndiaStory(Base):
    __tablename__ = "hidden_india_stories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    tagline: Mapped[str] = mapped_column(String(300))
    layer_discover: Mapped[dict] = mapped_column(JSONType)
    layer_experience: Mapped[dict] = mapped_column(JSONType)
    layer_explore: Mapped[dict] = mapped_column(JSONType)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    destination = relationship("Destination", back_populates="hidden_india_story")
    images = relationship("StoryImage", back_populates="hidden_india_story")

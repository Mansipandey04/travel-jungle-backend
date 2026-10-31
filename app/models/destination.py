from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db import Base

JSONType = JSON().with_variant(JSONB(), "postgresql")


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    region: Mapped[str] = mapped_column(String(120))
    state: Mapped[str] = mapped_column(String(120))
    summary: Mapped[str] = mapped_column(Text)
    hero_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    editorial: Mapped[dict | None] = mapped_column(JSONType, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    trips = relationship("Trip", back_populates="destination")
    events = relationship("Event", back_populates="destination")
    hidden_india_story = relationship("HiddenIndiaStory", back_populates="destination", uselist=False)
    travel_stories = relationship("TravelStory", back_populates="destination")

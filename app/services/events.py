from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.repositories.events import EventRepository
from app.schemas.common import clamp_pagination
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, db: Session) -> None:
        self.repo = EventRepository(db)

    def list_public(self, page: int = 1, page_size: int = 20):
        page, page_size = clamp_pagination(page, page_size)
        return self.repo.list_paginated(page=page, page_size=page_size, published_only=True)

    def get_public(self, slug: str) -> Event:
        event = self.repo.get_by_slug(slug)
        if not event or not event.is_published:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event

    def create(self, data: EventCreate) -> Event:
        if self.repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already exists")
        return self.repo.add(Event(**data.model_dump()))

    def update(self, id_: int, data: EventUpdate) -> Event:
        event = self.repo.get(id_)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(event, k, v)
        return self.repo.save(event)

    def delete(self, id_: int) -> None:
        event = self.repo.get(id_)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        self.repo.delete(event)

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.repositories.destinations import DestinationRepository
from app.schemas.common import clamp_pagination
from app.schemas.destination import DestinationCreate, DestinationUpdate


class DestinationService:
    def __init__(self, db: Session) -> None:
        self.repo = DestinationRepository(db)

    def list_public(self, page: int = 1, page_size: int = 20):
        page, page_size = clamp_pagination(page, page_size)
        return self.repo.list_paginated(page=page, page_size=page_size, published_only=True)

    def get_public(self, slug: str) -> Destination:
        dest = self.repo.get_by_slug(slug)
        if not dest or not dest.is_published:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
        return dest

    def create(self, data: DestinationCreate) -> Destination:
        if self.repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already exists")
        return self.repo.add(Destination(**data.model_dump()))

    def update(self, id_: int, data: DestinationUpdate) -> Destination:
        dest = self.repo.get(id_)
        if not dest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(dest, k, v)
        return self.repo.save(dest)

    def delete(self, id_: int) -> None:
        dest = self.repo.get(id_)
        if not dest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
        self.repo.delete(dest)

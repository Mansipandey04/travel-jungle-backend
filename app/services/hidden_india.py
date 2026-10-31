from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.hidden_india import HiddenIndiaStory
from app.repositories.destinations import DestinationRepository
from app.repositories.hidden_india import HiddenIndiaRepository
from app.schemas.common import clamp_pagination
from app.schemas.hidden_india import HiddenIndiaCreate, HiddenIndiaUpdate


def _layer_dump(value):
    return value.model_dump() if hasattr(value, "model_dump") else value


class HiddenIndiaService:
    def __init__(self, db: Session) -> None:
        self.repo = HiddenIndiaRepository(db)
        self.destinations = DestinationRepository(db)

    def list_public(self, page: int = 1, page_size: int = 20):
        page, page_size = clamp_pagination(page, page_size)
        return self.repo.list_paginated(page=page, page_size=page_size, published_only=True)

    def get_public(self, slug: str) -> HiddenIndiaStory:
        story = self.repo.get_by_slug(slug)
        if not story or not story.is_published:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hidden India story not found")
        return story

    def create(self, data: HiddenIndiaCreate) -> HiddenIndiaStory:
        if not self.destinations.get(data.destination_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid destination_id")
        if self.repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already exists")
        payload = data.model_dump()
        payload["layer_discover"] = _layer_dump(data.layer_discover)
        payload["layer_experience"] = _layer_dump(data.layer_experience)
        payload["layer_explore"] = _layer_dump(data.layer_explore)
        return self.repo.add(HiddenIndiaStory(**payload))

    def update(self, id_: int, data: HiddenIndiaUpdate) -> HiddenIndiaStory:
        story = self.repo.get(id_)
        if not story:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hidden India story not found")
        payload = data.model_dump(exclude_unset=True)
        for key in ("layer_discover", "layer_experience", "layer_explore"):
            if key in payload and payload[key] is not None:
                payload[key] = _layer_dump(payload[key])
        for k, v in payload.items():
            setattr(story, k, v)
        return self.repo.save(story)

    def delete(self, id_: int) -> None:
        story = self.repo.get(id_)
        if not story:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hidden India story not found")
        self.repo.delete(story)

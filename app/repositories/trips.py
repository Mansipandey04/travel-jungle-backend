from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.repositories.base import BaseRepository


class TripRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Trip)

    def list_by_destination(
        self, *, destination_id: int | None, page: int, page_size: int, published_only: bool = True
    ) -> tuple[list[Trip], int]:
        filters = []
        if destination_id is not None:
            filters.append(Trip.destination_id == destination_id)
        return self.list_paginated(page=page, page_size=page_size, published_only=published_only, extra_filters=filters)

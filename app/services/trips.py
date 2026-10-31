from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.repositories.destinations import DestinationRepository
from app.repositories.trips import TripRepository
from app.schemas.common import clamp_pagination
from app.schemas.trip import TripCreate, TripUpdate


class TripService:
    def __init__(self, db: Session) -> None:
        self.repo = TripRepository(db)
        self.destinations = DestinationRepository(db)

    def list_public(self, page: int = 1, page_size: int = 20, destination_slug: str | None = None):
        page, page_size = clamp_pagination(page, page_size)
        destination_id = None
        if destination_slug:
            dest = self.destinations.get_by_slug(destination_slug)
            if not dest:
                return [], 0
            destination_id = dest.id
        return self.repo.list_by_destination(
            destination_id=destination_id, page=page, page_size=page_size, published_only=True
        )

    def get_public(self, slug: str) -> Trip:
        trip = self.repo.get_by_slug(slug)
        if not trip or not trip.is_published:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        return trip

    def create(self, data: TripCreate) -> Trip:
        if not self.destinations.get(data.destination_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid destination_id")
        if self.repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already exists")
        payload = data.model_dump()
        if payload.get("itinerary"):
            payload["itinerary"] = [
                d.model_dump() if hasattr(d, "model_dump") else d for d in payload["itinerary"]
            ]
        return self.repo.add(Trip(**payload))

    def update(self, id_: int, data: TripUpdate) -> Trip:
        trip = self.repo.get(id_)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        payload = data.model_dump(exclude_unset=True)
        if "itinerary" in payload and payload["itinerary"] is not None:
            payload["itinerary"] = [
                d.model_dump() if hasattr(d, "model_dump") else d for d in payload["itinerary"]
            ]
        for k, v in payload.items():
            setattr(trip, k, v)
        return self.repo.save(trip)

    def delete(self, id_: int) -> None:
        trip = self.repo.get(id_)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        self.repo.delete(trip)

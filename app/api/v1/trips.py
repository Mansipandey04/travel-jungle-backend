from fastapi import APIRouter, Query

from app.deps import DbSession
from app.schemas.common import Page, PageMeta
from app.schemas.trip import TripOut
from app.services.trips import TripService

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("", response_model=Page[TripOut])
def list_trips(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    destination: str | None = Query(None, description="Destination slug filter"),
):
    items, total = TripService(db).list_public(page=page, page_size=page_size, destination_slug=destination)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{slug}", response_model=TripOut)
def get_trip(slug: str, db: DbSession):
    return TripService(db).get_public(slug)

from fastapi import APIRouter, Query

from app.deps import DbSession
from app.schemas.common import Page, PageMeta
from app.schemas.event import EventOut
from app.services.events import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=Page[EventOut])
def list_events(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    items, total = EventService(db).list_public(page=page, page_size=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{slug}", response_model=EventOut)
def get_event(slug: str, db: DbSession):
    return EventService(db).get_public(slug)

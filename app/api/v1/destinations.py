from fastapi import APIRouter, Query

from app.deps import DbSession
from app.schemas.common import Page, PageMeta
from app.schemas.destination import DestinationOut
from app.services.destinations import DestinationService

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("", response_model=Page[DestinationOut])
def list_destinations(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    items, total = DestinationService(db).list_public(page=page, page_size=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{slug}", response_model=DestinationOut)
def get_destination(slug: str, db: DbSession):
    return DestinationService(db).get_public(slug)

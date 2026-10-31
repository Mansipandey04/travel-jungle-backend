from fastapi import APIRouter, Query

from app.deps import DbSession
from app.schemas.common import Page, PageMeta
from app.schemas.hidden_india import HiddenIndiaOut
from app.services.hidden_india import HiddenIndiaService

router = APIRouter(prefix="/hidden-india", tags=["hidden-india"])


@router.get("", response_model=Page[HiddenIndiaOut])
def list_hidden_india(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    items, total = HiddenIndiaService(db).list_public(page=page, page_size=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{slug}", response_model=HiddenIndiaOut)
def get_hidden_india(slug: str, db: DbSession):
    return HiddenIndiaService(db).get_public(slug)

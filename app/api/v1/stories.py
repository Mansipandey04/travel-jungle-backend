from fastapi import APIRouter, Query

from app.deps import DbSession
from app.schemas.common import Page, PageMeta
from app.schemas.story import StoryOut
from app.services.stories import StoryService

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("", response_model=Page[StoryOut])
def list_stories(
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    items, total = StoryService(db).list_public(page=page, page_size=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{slug}", response_model=StoryOut)
def get_story(slug: str, db: DbSession):
    return StoryService(db).get_public(slug)

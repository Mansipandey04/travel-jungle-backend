from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.story import StorySource, StoryStatus, TravelStory
from app.repositories.base import BaseRepository


class StoryRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, TravelStory)

    def list_public(self, *, page: int, page_size: int) -> tuple[list[TravelStory], int]:
        from sqlalchemy import func, or_

        public_filter = or_(
            TravelStory.status == StoryStatus.approved.value,
            TravelStory.source == StorySource.editorial.value,
        )
        # Public reads: approved (any source) OR editorial that is approved
        stmt = select(TravelStory).where(TravelStory.status == StoryStatus.approved.value)
        count_stmt = select(func.count()).select_from(TravelStory).where(
            TravelStory.status == StoryStatus.approved.value
        )
        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all())
        return items, total

    def list_all(self, *, page: int, page_size: int, status: str | None = None) -> tuple[list[TravelStory], int]:
        from sqlalchemy import func

        stmt = select(TravelStory)
        count_stmt = select(func.count()).select_from(TravelStory)
        if status:
            stmt = stmt.where(TravelStory.status == status)
            count_stmt = count_stmt.where(TravelStory.status == status)
        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all())
        return items, total

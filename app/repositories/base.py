from typing import Any, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository:
    def __init__(self, db: Session, model: type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get(self, id_: int) -> Any | None:
        return self.db.get(self.model, id_)

    def get_by_slug(self, slug: str) -> Any | None:
        return self.db.scalar(select(self.model).where(self.model.slug == slug))  # type: ignore[attr-defined]

    def list_paginated(
        self,
        *,
        page: int,
        page_size: int,
        published_only: bool = True,
        extra_filters: list | None = None,
    ) -> tuple[list, int]:
        stmt = select(self.model)
        count_stmt = select(func.count()).select_from(self.model)
        if published_only and hasattr(self.model, "is_published"):
            stmt = stmt.where(self.model.is_published.is_(True))  # type: ignore[attr-defined]
            count_stmt = count_stmt.where(self.model.is_published.is_(True))  # type: ignore[attr-defined]
        if extra_filters:
            for f in extra_filters:
                stmt = stmt.where(f)
                count_stmt = count_stmt.where(f)
        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all())
        return items, total

    def add(self, obj: Any) -> Any:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Any) -> None:
        self.db.delete(obj)
        self.db.commit()

    def save(self, obj: Any) -> Any:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

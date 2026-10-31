from sqlalchemy.orm import Session

from app.models.event import Event
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Event)

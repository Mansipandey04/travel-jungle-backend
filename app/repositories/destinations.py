from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.repositories.base import BaseRepository


class DestinationRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Destination)

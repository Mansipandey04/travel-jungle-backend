from sqlalchemy.orm import Session

from app.models.hidden_india import HiddenIndiaStory
from app.repositories.base import BaseRepository


class HiddenIndiaRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, HiddenIndiaStory)

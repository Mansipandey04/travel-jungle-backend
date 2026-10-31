from sqlalchemy.orm import Session

from app.models.contact import ContactMessage
from app.repositories.base import BaseRepository


class ContactRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ContactMessage)

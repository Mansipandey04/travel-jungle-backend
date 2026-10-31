from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.repositories.base import BaseRepository


class EnquiryRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Enquiry)

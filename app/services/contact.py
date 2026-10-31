from sqlalchemy.orm import Session

from app.models.contact import ContactMessage
from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactCreate
from app.utils import strip_html


class ContactService:
    def __init__(self, db: Session) -> None:
        self.repo = ContactRepository(db)

    def create(self, data: ContactCreate) -> ContactMessage:
        return self.repo.add(
            ContactMessage(
                name=strip_html(data.name).strip(),
                email=str(data.email).lower(),
                subject=strip_html(data.subject).strip(),
                message=strip_html(data.message).strip(),
            )
        )

from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.repositories.enquiries import EnquiryRepository
from app.schemas.enquiry import EnquiryCreate
from app.utils import strip_html


class EnquiryService:
    def __init__(self, db: Session) -> None:
        self.repo = EnquiryRepository(db)

    def create(self, data: EnquiryCreate) -> Enquiry:
        return self.repo.add(
            Enquiry(
                name=strip_html(data.name).strip(),
                email=str(data.email).lower(),
                phone=data.phone,
                message=strip_html(data.message).strip(),
                source_type=data.source_type,
                source_id=data.source_id,
            )
        )

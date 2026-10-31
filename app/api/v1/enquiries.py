from fastapi import APIRouter, Depends, status

from app.deps import DbSession
from app.rate_limit import rate_limit_submissions
from app.schemas.enquiry import EnquiryCreate, EnquiryOut
from app.services.enquiries import EnquiryService

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


@router.post(
    "",
    response_model=EnquiryOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_submissions)],
)
def create_enquiry(payload: EnquiryCreate, db: DbSession):
    return EnquiryService(db).create(payload)

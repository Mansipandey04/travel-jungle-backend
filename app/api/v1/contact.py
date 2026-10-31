from fastapi import APIRouter, Depends, status

from app.deps import DbSession
from app.rate_limit import rate_limit_submissions
from app.schemas.contact import ContactCreate, ContactOut
from app.services.contact import ContactService

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post(
    "",
    response_model=ContactOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_submissions)],
)
def create_contact(payload: ContactCreate, db: DbSession):
    return ContactService(db).create(payload)

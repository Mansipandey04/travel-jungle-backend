from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.config import get_settings
from app.deps import AdminUser, DbSession, StorageDep
from app.schemas.common import MessageOut, Page, PageMeta
from app.schemas.destination import DestinationCreate, DestinationOut, DestinationUpdate
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.schemas.hidden_india import HiddenIndiaCreate, HiddenIndiaOut, HiddenIndiaUpdate
from app.schemas.story import StoryAdminCreate, StoryModerate, StoryOut
from app.schemas.trip import TripCreate, TripOut, TripUpdate
from app.services.destinations import DestinationService
from app.services.events import EventService
from app.services.hidden_india import HiddenIndiaService
from app.services.stories import StoryService
from app.services.trips import TripService
from app.storage.local import ALLOWED_MIME

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/destinations", response_model=DestinationOut, status_code=status.HTTP_201_CREATED)
def create_destination(payload: DestinationCreate, db: DbSession, _: AdminUser):
    return DestinationService(db).create(payload)


@router.patch("/destinations/{id_}", response_model=DestinationOut)
def update_destination(id_: int, payload: DestinationUpdate, db: DbSession, _: AdminUser):
    return DestinationService(db).update(id_, payload)


@router.delete("/destinations/{id_}", response_model=MessageOut)
def delete_destination(id_: int, db: DbSession, _: AdminUser):
    DestinationService(db).delete(id_)
    return MessageOut(message="deleted")


@router.post("/trips", response_model=TripOut, status_code=status.HTTP_201_CREATED)
def create_trip(payload: TripCreate, db: DbSession, _: AdminUser):
    return TripService(db).create(payload)


@router.patch("/trips/{id_}", response_model=TripOut)
def update_trip(id_: int, payload: TripUpdate, db: DbSession, _: AdminUser):
    return TripService(db).update(id_, payload)


@router.delete("/trips/{id_}", response_model=MessageOut)
def delete_trip(id_: int, db: DbSession, _: AdminUser):
    TripService(db).delete(id_)
    return MessageOut(message="deleted")


@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: DbSession, _: AdminUser):
    return EventService(db).create(payload)


@router.patch("/events/{id_}", response_model=EventOut)
def update_event(id_: int, payload: EventUpdate, db: DbSession, _: AdminUser):
    return EventService(db).update(id_, payload)


@router.delete("/events/{id_}", response_model=MessageOut)
def delete_event(id_: int, db: DbSession, _: AdminUser):
    EventService(db).delete(id_)
    return MessageOut(message="deleted")


@router.post("/hidden-india", response_model=HiddenIndiaOut, status_code=status.HTTP_201_CREATED)
def create_hidden_india(payload: HiddenIndiaCreate, db: DbSession, _: AdminUser):
    return HiddenIndiaService(db).create(payload)


@router.patch("/hidden-india/{id_}", response_model=HiddenIndiaOut)
def update_hidden_india(id_: int, payload: HiddenIndiaUpdate, db: DbSession, _: AdminUser):
    return HiddenIndiaService(db).update(id_, payload)


@router.delete("/hidden-india/{id_}", response_model=MessageOut)
def delete_hidden_india(id_: int, db: DbSession, _: AdminUser):
    HiddenIndiaService(db).delete(id_)
    return MessageOut(message="deleted")


@router.get("/stories", response_model=Page[StoryOut])
def list_admin_stories(
    db: DbSession,
    _: AdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status_filter: str | None = Query(None, alias="status"),
):
    items, total = StoryService(db).list_admin(page=page, page_size=page_size, status=status_filter)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.post("/stories", response_model=StoryOut, status_code=status.HTTP_201_CREATED)
def create_admin_story(payload: StoryAdminCreate, db: DbSession, _: AdminUser):
    return StoryService(db).create_admin(payload)


@router.patch("/stories/{id_}", response_model=StoryOut)
def moderate_story(id_: int, payload: StoryModerate, db: DbSession, _: AdminUser):
    return StoryService(db).moderate(id_, payload)


@router.post("/upload")
async def upload_image(storage: StorageDep, _: AdminUser, file: UploadFile = File(...)):
    settings = get_settings()
    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")
    data = await file.read()
    if len(data) > settings.upload_max_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
    try:
        url = storage.save(filename=file.filename or "upload", content=data, content_type=content_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"url": url}

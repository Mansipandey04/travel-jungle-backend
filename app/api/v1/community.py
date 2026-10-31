from fastapi import APIRouter, Depends, status

from app.deps import DbSession
from app.rate_limit import rate_limit_submissions
from app.schemas.story import CommunityStoryCreate, StoryOut
from app.services.stories import StoryService

router = APIRouter(prefix="/community", tags=["community"])


@router.post(
    "/stories",
    response_model=StoryOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_submissions)],
)
def submit_community_story(payload: CommunityStoryCreate, db: DbSession):
    return StoryService(db).submit_community(payload)

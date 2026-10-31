from app.models.story import StoryStatus
from app.schemas.story import CommunityStoryCreate
from app.services.stories import StoryService


def test_community_defaults_pending(db_session):
    story = StoryService(db_session).submit_community(
        CommunityStoryCreate(title="Hello", body_md="World", author_display="A")
    )
    assert story.status == StoryStatus.pending.value
    assert story.source == "community"

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.story import StorySource, StoryStatus, TravelStory
from app.repositories.destinations import DestinationRepository
from app.repositories.stories import StoryRepository
from app.schemas.common import clamp_pagination
from app.schemas.story import CommunityStoryCreate, StoryAdminCreate, StoryModerate
from app.utils import slugify, strip_html


class StoryService:
    def __init__(self, db: Session) -> None:
        self.repo = StoryRepository(db)
        self.destinations = DestinationRepository(db)

    def list_public(self, page: int = 1, page_size: int = 20):
        page, page_size = clamp_pagination(page, page_size)
        return self.repo.list_public(page=page, page_size=page_size)

    def get_public(self, slug: str) -> TravelStory:
        story = self.repo.get_by_slug(slug)
        if not story or story.status != StoryStatus.approved.value:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
        return story

    def submit_community(self, data: CommunityStoryCreate) -> TravelStory:
        """Community submissions always start as pending."""
        destination_id = None
        if data.destination_slug:
            dest = self.destinations.get_by_slug(data.destination_slug)
            if dest:
                destination_id = dest.id
        base_slug = data.slug or slugify(data.title)
        slug = base_slug
        n = 1
        while self.repo.get_by_slug(slug):
            n += 1
            slug = f"{base_slug}-{n}"
        story = TravelStory(
            slug=slug,
            destination_id=destination_id,
            title=strip_html(data.title).strip(),
            body_md=strip_html(data.body_md).strip(),
            author_display=strip_html(data.author_display).strip(),
            status=StoryStatus.pending.value,
            source=StorySource.community.value,
            is_demo=False,
        )
        return self.repo.add(story)

    def list_admin(self, page: int = 1, page_size: int = 20, status: str | None = None):
        page, page_size = clamp_pagination(page, page_size)
        return self.repo.list_all(page=page, page_size=page_size, status=status)

    def moderate(self, id_: int, data: StoryModerate) -> TravelStory:
        story = self.repo.get(id_)
        if not story:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
        story.status = data.status.value
        return self.repo.save(story)

    def create_admin(self, data: StoryAdminCreate) -> TravelStory:
        if self.repo.get_by_slug(data.slug):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already exists")
        return self.repo.add(
            TravelStory(
                slug=data.slug,
                destination_id=data.destination_id,
                title=data.title,
                body_md=data.body_md,
                author_display=data.author_display,
                status=data.status.value,
                source=data.source.value,
                is_demo=data.is_demo,
            )
        )

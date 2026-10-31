from app.models.story import StoryStatus, TravelStory
from sqlalchemy import select


def test_community_submit_pending(client, db_session):
    r = client.post(
        "/api/v1/community/stories",
        json={
            "title": "My <b>Meghalaya</b> Walk",
            "body_md": "A careful walk near living roots.",
            "author_display": "Traveller",
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == StoryStatus.pending.value
    assert body["source"] == "community"
    assert "<b>" not in body["title"]

    stored = db_session.scalar(select(TravelStory).where(TravelStory.slug == body["slug"]))
    assert stored is not None
    assert stored.status == "pending"

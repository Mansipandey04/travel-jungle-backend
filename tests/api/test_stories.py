from app.models.story import StorySource, StoryStatus, TravelStory


def test_public_stories_only_approved(client, db_session):
    db_session.add_all(
        [
            TravelStory(
                slug="approved-story",
                title="Approved",
                body_md="Body",
                author_display="Editor",
                status=StoryStatus.approved.value,
                source=StorySource.editorial.value,
                is_demo=True,
            ),
            TravelStory(
                slug="pending-story",
                title="Pending",
                body_md="Body",
                author_display="Guest",
                status=StoryStatus.pending.value,
                source=StorySource.community.value,
                is_demo=False,
            ),
        ]
    )
    db_session.commit()
    r = client.get("/api/v1/stories")
    assert r.json()["meta"]["total"] == 1
    assert client.get("/api/v1/stories/pending-story").status_code == 404
    assert client.get("/api/v1/stories/approved-story").status_code == 200

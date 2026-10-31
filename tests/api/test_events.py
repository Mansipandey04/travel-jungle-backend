from app.models.event import Event


def test_events(client, db_session):
    db_session.add(
        Event(
            slug="demo-event",
            title="Demo Festival Note",
            summary="Illustrative event without invented dates as live bookings.",
            is_published=True,
            is_demo=True,
        )
    )
    db_session.commit()
    assert client.get("/api/v1/events").json()["meta"]["total"] == 1
    assert client.get("/api/v1/events/demo-event").status_code == 200
    assert client.get("/api/v1/events/nope").status_code == 404

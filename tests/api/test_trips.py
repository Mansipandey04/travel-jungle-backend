from app.models.destination import Destination
from app.models.trip import Trip


def _dest(db):
    d = Destination(
        slug="majuli",
        name="Majuli",
        region="Northeast",
        state="Assam",
        summary="River island",
        is_published=True,
        is_demo=True,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def test_trips_list_and_filter(client, db_session):
    d = _dest(db_session)
    db_session.add(
        Trip(
            slug="demo-majuli",
            destination_id=d.id,
            title="Demo trip",
            summary="Illustrative",
            is_published=True,
            is_demo=True,
        )
    )
    db_session.commit()

    r = client.get("/api/v1/trips")
    assert r.status_code == 200
    assert r.json()["meta"]["total"] == 1

    r2 = client.get("/api/v1/trips?destination=majuli")
    assert r2.json()["meta"]["total"] == 1

    r3 = client.get("/api/v1/trips/demo-majuli")
    assert r3.status_code == 200
    assert r3.json()["is_demo"] is True

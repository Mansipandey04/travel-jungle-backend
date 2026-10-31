from app.models.destination import Destination


def test_list_destinations_empty(client):
    r = client.get("/api/v1/destinations")
    assert r.status_code == 200
    body = r.json()
    assert body["items"] == []
    assert body["meta"]["total"] == 0


def test_get_destination_404(client):
    r = client.get("/api/v1/destinations/missing")
    assert r.status_code == 404


def test_list_and_get_published(client, db_session):
    db_session.add(
        Destination(
            slug="hampi",
            name="Hampi",
            region="Deccan",
            state="Karnataka",
            summary="UNESCO site",
            is_published=True,
            is_demo=True,
        )
    )
    db_session.add(
        Destination(
            slug="draft",
            name="Draft",
            region="X",
            state="Y",
            summary="hidden",
            is_published=False,
            is_demo=True,
        )
    )
    db_session.commit()

    r = client.get("/api/v1/destinations")
    assert r.status_code == 200
    assert r.json()["meta"]["total"] == 1
    assert r.json()["items"][0]["slug"] == "hampi"

    r2 = client.get("/api/v1/destinations/hampi")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Hampi"

    r3 = client.get("/api/v1/destinations/draft")
    assert r3.status_code == 404

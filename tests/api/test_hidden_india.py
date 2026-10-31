from app.models.destination import Destination
from app.models.hidden_india import HiddenIndiaStory


def test_hidden_india(client, db_session):
    d = Destination(
        slug="ziro-valley",
        name="Ziro Valley",
        region="Northeast",
        state="Arunachal Pradesh",
        summary="Apatani plateau",
        is_published=True,
        is_demo=True,
    )
    db_session.add(d)
    db_session.commit()
    db_session.refresh(d)
    db_session.add(
        HiddenIndiaStory(
            slug="hidden-ziro",
            destination_id=d.id,
            title="Ziro",
            tagline="Apatani fields",
            layer_discover={"headline": "D", "body": "discover", "tips": [], "media_refs": []},
            layer_experience={"headline": "E", "body": "experience", "tips": [], "media_refs": []},
            layer_explore={"headline": "X", "body": "explore", "tips": [], "media_refs": []},
            is_published=True,
            is_demo=True,
        )
    )
    db_session.commit()

    r = client.get("/api/v1/hidden-india")
    assert r.status_code == 200
    assert r.json()["meta"]["total"] == 1
    detail = client.get("/api/v1/hidden-india/hidden-ziro").json()
    assert "layer_discover" in detail
    assert detail["is_demo"] is True

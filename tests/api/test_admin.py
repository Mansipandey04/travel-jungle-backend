from app.models.story import StorySource, StoryStatus, TravelStory


def test_admin_requires_auth(client):
    r = client.post(
        "/api/v1/admin/destinations",
        json={
            "slug": "x",
            "name": "X",
            "region": "R",
            "state": "S",
            "summary": "sum",
        },
    )
    assert r.status_code == 401


def test_admin_create_destination(client, admin_headers):
    r = client.post(
        "/api/v1/admin/destinations",
        headers=admin_headers,
        json={
            "slug": "shnongpdeng",
            "name": "Shnongpdeng",
            "region": "Northeast",
            "state": "Meghalaya",
            "summary": "Umngot river village",
            "is_demo": True,
        },
    )
    assert r.status_code == 201
    assert r.json()["slug"] == "shnongpdeng"


def test_auth_login_and_me(client, admin_headers):
    bad = client.post("/api/v1/auth/login", json={"token": "wrong"})
    assert bad.status_code == 401
    ok = client.post("/api/v1/auth/login", json={"token": "test-admin-token"})
    assert ok.status_code == 200
    assert ok.json()["token_type"] == "bearer"
    me = client.get("/api/v1/auth/me", headers=admin_headers)
    assert me.status_code == 200
    assert me.json()["authenticated"] is True


def test_moderate_story(client, db_session, admin_headers):
    db_session.add(
        TravelStory(
            slug="wait",
            title="Wait",
            body_md="Body",
            author_display="Guest",
            status=StoryStatus.pending.value,
            source=StorySource.community.value,
        )
    )
    db_session.commit()
    story_id = db_session.query(TravelStory).one().id
    r = client.patch(
        f"/api/v1/admin/stories/{story_id}",
        headers=admin_headers,
        json={"status": "approved"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "approved"
    assert client.get("/api/v1/stories/wait").status_code == 200


def test_upload(client, admin_headers, tmp_path):
    from app.deps import get_storage
    from app.main import app as fastapi_app
    from app.storage.local import LocalStorage

    storage = LocalStorage(root=str(tmp_path), public_base_url="http://testserver")
    fastapi_app.dependency_overrides[get_storage] = lambda: storage
    files = {"file": ("shot.png", b"\x89PNG\r\n\x1a\nfake", "image/png")}
    r = client.post("/api/v1/admin/upload", headers=admin_headers, files=files)
    assert r.status_code == 200
    assert r.json()["url"].startswith("http://testserver/uploads/")
    assert any(tmp_path.iterdir())
    fastapi_app.dependency_overrides.pop(get_storage, None)


def test_upload_unauthorized(client):
    files = {"file": ("shot.png", b"abc", "image/png")}
    r = client.post("/api/v1/admin/upload", files=files)
    assert r.status_code == 401

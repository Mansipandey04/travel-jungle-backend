import os

from app.config import get_settings
from app.rate_limit import limiter


def test_contact_rate_limited(client, monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_SUBMISSIONS_PER_MIN", "2")
    get_settings.cache_clear()
    limiter._hits.clear()
    payload = {
        "name": "A",
        "email": "a@example.com",
        "subject": "S",
        "message": "M",
    }
    assert client.post("/api/v1/contact", json=payload).status_code == 201
    assert client.post("/api/v1/contact", json=payload).status_code == 201
    assert client.post("/api/v1/contact", json=payload).status_code == 429
    monkeypatch.setenv("RATE_LIMIT_SUBMISSIONS_PER_MIN", "1000")
    get_settings.cache_clear()
    limiter._hits.clear()

def test_contact_create(client):
    r = client.post(
        "/api/v1/contact",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "subject": "Hello",
            "message": "India-only question.",
        },
    )
    assert r.status_code == 201
    assert r.json()["subject"] == "Hello"

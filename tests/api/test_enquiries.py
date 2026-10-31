def test_enquiry_create(client):
    r = client.post(
        "/api/v1/enquiries",
        json={
            "name": "Asha",
            "email": "asha@example.com",
            "message": "Curious about Tirthan Valley demo trip.",
            "source_type": "trip",
        },
    )
    assert r.status_code == 201
    assert r.json()["email"] == "asha@example.com"

def _auth_headers(client, email: str) -> dict:
    password = "secret123"
    client.post("/auth/register", json={"email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    token = login_response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_add_history_then_list_returns_saved_item(client):
    headers = _auth_headers(client, "history@test.com")
    create_payload = {
        "filename": "image_01.jpg",
        "status": "processed",
        "detectionCount": 2,
        "type": "image",
    }

    create_response = client.post("/history/", json=create_payload, headers=headers)

    assert create_response.status_code == 200
    create_data = create_response.json()
    assert create_data["message"] == "Saved"
    assert "id" in create_data

    list_response = client.get("/history/", headers=headers)

    assert list_response.status_code == 200
    rows = list_response.json()
    assert len(rows) == 1
    assert rows[0]["filename"] == "image_01.jpg"
    assert rows[0]["status"] == "processed"
    assert rows[0]["detectionCount"] == 2
    assert rows[0]["type"] == "image"


def test_history_is_isolated_per_user(client):
    headers_a = _auth_headers(client, "a@test.com")
    headers_b = _auth_headers(client, "b@test.com")

    client.post(
        "/history/",
        json={"filename": "a.jpg", "status": "done", "detectionCount": 1, "type": "Good"},
        headers=headers_a,
    )
    client.post(
        "/history/",
        json={"filename": "b.jpg", "status": "done", "detectionCount": 1, "type": "Broken"},
        headers=headers_b,
    )

    response_a = client.get("/history/", headers=headers_a)
    response_b = client.get("/history/", headers=headers_b)

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert len(response_a.json()) == 1
    assert len(response_b.json()) == 1
    assert response_a.json()[0]["filename"] == "a.jpg"
    assert response_b.json()[0]["filename"] == "b.jpg"

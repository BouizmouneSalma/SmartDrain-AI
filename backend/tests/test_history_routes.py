def test_add_history_then_list_returns_saved_item(client):
    create_payload = {
        "filename": "image_01.jpg",
        "status": "processed",
        "detectionCount": 2,
        "type": "image",
    }

    create_response = client.post("/history/", json=create_payload)

    assert create_response.status_code == 200
    create_data = create_response.json()
    assert create_data["message"] == "Saved"
    assert "id" in create_data

    list_response = client.get("/history/")

    assert list_response.status_code == 200
    rows = list_response.json()
    assert len(rows) == 1
    assert rows[0]["filename"] == "image_01.jpg"
    assert rows[0]["status"] == "processed"
    assert rows[0]["detectionCount"] == 2
    assert rows[0]["type"] == "image"

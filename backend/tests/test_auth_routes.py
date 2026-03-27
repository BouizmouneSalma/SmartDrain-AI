def test_register_success(client):
    payload = {"email": "User@Test.com", "password": "secret123"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created"
    assert data["email"] == "user@test.com"
    assert "id" in data


def test_register_duplicate_user_returns_400(client):
    payload = {"email": "duplicate@test.com", "password": "secret123"}
    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@test.com", "password": "secret123"})

    response = client.post("/auth/login", json={"email": "login@test.com", "password": "secret123"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["token"].startswith("u.")


def test_login_invalid_credentials_returns_401(client):
    client.post("/auth/register", json={"email": "invalid@test.com", "password": "secret123"})

    response = client.post("/auth/login", json={"email": "invalid@test.com", "password": "wrong-pass"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_tokens_are_user_specific(client):
    client.post("/auth/register", json={"email": "user1@test.com", "password": "secret123"})
    client.post("/auth/register", json={"email": "user2@test.com", "password": "secret123"})

    login_1 = client.post("/auth/login", json={"email": "user1@test.com", "password": "secret123"})
    login_2 = client.post("/auth/login", json={"email": "user2@test.com", "password": "secret123"})

    assert login_1.status_code == 200
    assert login_2.status_code == 200
    assert login_1.json()["token"] != login_2.json()["token"]

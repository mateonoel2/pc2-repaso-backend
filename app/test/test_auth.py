def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "testuser@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_register_existing_email(client):
    client.post(
        "/api/auth/register",
        json={"email": "existinguser@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "existinguser@example.com", "password": "newpassword456"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado"


def test_register_invalid_email(client):
    response = client.post(
        "/api/auth/register", json={"email": "invalidemail", "password": "password123"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text


def test_register_missing_password(client):
    response = client.post("/api/auth/register", json={"email": "user@example.com"})
    assert response.status_code == 422
    assert "field required" in response.text


def test_register_empty_email(client):
    response = client.post(
        "/api/auth/register", json={"email": "", "password": "password123"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text


def test_register_short_password(client):
    response = client.post(
        "/api/auth/register", json={"email": "user@example.com", "password": "123"}
    )
    assert response.status_code == 200


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_incorrect_password(client):
    client.post(
        "/api/auth/register",
        json={"email": "wrongpassuser@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "wrongpassuser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"


def test_login_nonexistent_email(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"


def test_login_empty_email(client):
    response = client.post(
        "/api/auth/login", json={"email": "", "password": "password123"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text


def test_login_empty_password(client):
    response = client.post(
        "/api/auth/login", json={"email": "user@example.com", "password": ""}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"


def test_login_invalid_email_format(client):
    response = client.post(
        "/api/auth/login", json={"email": "invalidemail", "password": "password123"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text


def test_register_server_error(client, monkeypatch):
    def mock_get_db():
        raise Exception("Database connection error")

    monkeypatch.setattr("dependencies.get_db", mock_get_db)
    response = client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert response.status_code == 500
    assert "Internal Server Error" in response.text

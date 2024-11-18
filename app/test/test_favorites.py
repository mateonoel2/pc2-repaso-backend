def test_add_to_favorites_success(client, auth_headers):
    response = client.post(
        "/api/user/favorites", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Anime agregado a favoritos"


def test_add_to_favorites_nonexistent_anime(client, auth_headers):
    response = client.post(
        "/api/user/favorites", json={"anime_id": 9999}, headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime no encontrado"


def test_add_to_favorites_already_added(client, auth_headers):
    client.post("/api/user/favorites", json={"anime_id": 1}, headers=auth_headers)
    response = client.post(
        "/api/user/favorites", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El anime ya está en favoritos"


def test_add_to_favorites_unauthorized(client):
    response = client.post("/api/user/favorites", json={"anime_id": 1})
    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudieron validar las credenciales"


def test_add_to_favorites_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.post("/api/user/favorites", json={"anime_id": 1}, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudieron validar las credenciales"


def test_remove_from_favorites_success(client, auth_headers):
    client.post("/api/user/favorites", json={"anime_id": 1}, headers=auth_headers)
    response = client.delete(
        "/api/user/favorites", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Anime removido de favoritos"


def test_remove_from_favorites_not_in_favorites(client, auth_headers):
    response = client.delete(
        "/api/user/favorites", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El anime no está en favoritos"


def test_remove_from_favorites_nonexistent_anime(client, auth_headers):
    response = client.delete(
        "/api/user/favorites", json={"anime_id": 9999}, headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime no encontrado"


def test_remove_from_favorites_unauthorized(client):
    response = client.delete("/api/user/favorites", json={"anime_id": 1})
    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudieron validar las credenciales"


def test_favorites_server_error(client, auth_headers, monkeypatch):
    def mock_commit():
        raise Exception("Database commit error")

    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_commit)
    response = client.post(
        "/api/user/favorites", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 500
    assert "Internal Server Error" in response.text

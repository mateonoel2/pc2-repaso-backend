def test_add_to_history_success(client, auth_headers):
    response = client.post(
        "/api/user/history",
        json={"anime_id": 1, "status": "visto"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Anime agregado/actualizado en el historial"


def test_add_to_history_invalid_status(client, auth_headers):
    response = client.post(
        "/api/user/history",
        json={"anime_id": 1, "status": "completado"},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Estado inválido"


def test_add_to_history_nonexistent_anime(client, auth_headers):
    response = client.post(
        "/api/user/history",
        json={"anime_id": 9999, "status": "visto"},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime no encontrado"


def test_add_to_history_unauthorized(client):
    response = client.post("/api/user/history", json={"anime_id": 1, "status": "visto"})
    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudieron validar las credenciales"


def test_remove_from_history_success(client, auth_headers):
    client.post(
        "/api/user/history",
        json={"anime_id": 1, "status": "visto"},
        headers=auth_headers,
    )
    response = client.delete(
        "/api/user/history", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Anime removido del historial"


def test_remove_from_history_not_in_history(client, auth_headers):
    response = client.delete(
        "/api/user/history", json={"anime_id": 1}, headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime no encontrado en el historial"


def test_remove_from_history_nonexistent_anime(client, auth_headers):
    response = client.delete(
        "/api/user/history", json={"anime_id": 9999}, headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime no encontrado en el historial"


def test_remove_from_history_unauthorized(client):
    response = client.delete("/api/user/history", json={"anime_id": 1})
    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudieron validar las credenciales"


def test_history_server_error(client, auth_headers, monkeypatch):
    def mock_commit():
        raise Exception("Database commit error")

    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_commit)
    response = client.post(
        "/api/user/history",
        json={"anime_id": 1, "status": "visto"},
        headers=auth_headers,
    )
    assert response.status_code == 500
    assert "Internal Server Error" in response.text

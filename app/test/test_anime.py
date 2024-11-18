def test_get_anime_list_success(client):
    response = client.get("/api/anime/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 20


def test_get_anime_list_no_animes(client, monkeypatch):
    def mock_query(*args, **kwargs):
        class MockQuery:
            def limit(self, *args, **kwargs):
                return self

            def all(self):
                return []

        return MockQuery()

    monkeypatch.setattr("sqlalchemy.orm.Session.query", mock_query)
    response = client.get("/api/anime/list")
    assert response.status_code == 200
    assert response.json() == []


def test_get_anime_list_invalid_method(client):
    response = client.post("/api/anime/list")
    assert response.status_code == 405


def test_get_anime_list_server_error(client, monkeypatch):
    def mock_query(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr("sqlalchemy.orm.Session.query", mock_query)
    response = client.get("/api/anime/list")
    assert response.status_code == 500
    assert "Internal Server Error" in response.text

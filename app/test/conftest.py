import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers(client):
    client.post(
        "/api/auth/register",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers

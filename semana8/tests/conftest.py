import pytest
from fastapi.testclient import TestClient
from app.main import app  # asegúrate de tener app.main

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_user_generic():
    return {"nombre": "Usuario Test", "email": "test@example.com", "password": "123456"}

@pytest.fixture
def authenticated_client(client, sample_user_generic):
    # Si tienes endpoints /auth/register y /auth/login, llámalos aquí
    client.post("/auth/register", json=sample_user_generic)
    class AuthClient:
        def __init__(self, c):
            self.client = c
        def get(self, *a, **k): return self.client.get(*a, **k)
        def post(self, *a, **k): return self.client.post(*a, **k)
        def put(self, *a, **k): return self.client.put(*a, **k)
        def delete(self, *a, **k): return self.client.delete(*a, **k)
    return AuthClient(client)

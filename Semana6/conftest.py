import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from semana7.app.main import app   # 👈 solo app desde main
from database import Base, get_db   # 👈 get_db ahora viene de database.py

# Base de datos de prueba personalizada para Rent a Car
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rental.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Fixture con datos de ejemplo para Rent a Car
@pytest.fixture
def sample_alquiler_data():
    return {
        "cliente": "Carlos Pérez",
        "vehiculo": "Mazda CX-5",
        "fecha_inicio": "2025-10-01",
        "fecha_fin": "2025-10-05",
        "precio_diario": 120000,
        "licencia_valida": True,
        "edad_conductor": 28
    }

@pytest.fixture
def auth_headers(client):
    """Headers de autenticación para tests"""
    # Registrar usuario admin de Rent a Car
    client.post("/auth/register", json={
        "username": "admin_rental",
        "password": "test123",
        "role": "admin_rental"
    })

    login_response = client.post("/auth/login", data={
        "username": "admin_rental",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

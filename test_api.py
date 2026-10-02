import os
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_and_home():
    r = client.post("/api/register", json={"name":"Test User","email":"test@example.com","password":"password123"})
    assert r.status_code == 200
    r = client.post("/api/generate-home", json={
        "budget": 50000,
        "rooms": ["Living Room"],
        "style": "Modern",
        "notes": "",
        "quantities": {}
    })
    assert r.status_code == 200
    data = r.json()
    assert data["budget"] == 50000
    assert data["estimated_total"] <= 50000


def test_login():
    r = client.post("/api/logout")
    assert r.status_code == 200
    r = client.post("/api/login", json={"email":"test@example.com","password":"password123"})
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "test@example.com"

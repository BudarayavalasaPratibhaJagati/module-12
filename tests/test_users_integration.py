import uuid

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user_creates_user():
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "secret123"

    resp = client.post(
        "/users/register",
        json={"email": email, "password": password},
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == email
    assert "id" in data


def test_login_after_register():
    email = f"user_login_{uuid.uuid4().hex}@example.com"
    password = "secret123"

    reg = client.post(
        "/users/register",
        json={"email": email, "password": password},
    )
    assert reg.status_code == 201

    login = client.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200
    data = login.json()
    assert data["user"]["email"] == email
    assert data["message"] == "Login successful"

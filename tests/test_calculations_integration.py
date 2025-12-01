from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_read_calculation():
    create = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert create.status_code == 201
    data = create.json()
    calc_id = data["id"]
    assert data["result"] == 15

    read = client.get(f"/calculations/{calc_id}")
    assert read.status_code == 200
    read_data = read.json()
    assert read_data["id"] == calc_id
    assert read_data["result"] == 15


def test_update_calculation():
    create = client.post(
        "/calculations/",
        json={"a": 2, "b": 3, "type": "Multiply"},
    )
    assert create.status_code == 201
    calc_id = create.json()["id"]

    update = client.put(
        f"/calculations/{calc_id}",
        json={"a": 10, "b": 4, "type": "Sub"},
    )
    assert update.status_code == 200
    data = update.json()
    assert data["result"] == 6  # 10 - 4


def test_delete_calculation():
    create = client.post(
        "/calculations/",
        json={"a": 100, "b": 25, "type": "Divide"},
    )
    assert create.status_code == 201
    calc_id = create.json()["id"]

    delete = client.delete(f"/calculations/{calc_id}")
    assert delete.status_code == 204

    read = client.get(f"/calculations/{calc_id}")
    assert read.status_code == 404


def test_divide_by_zero_invalid():
    resp = client.post(
        "/calculations/",
        json={"a": 10, "b": 0, "type": "Divide"},
    )
    # Pydantic body validation failure -> FastAPI returns 422
    assert resp.status_code == 422
    body = resp.json()
    # optional: basic check that it mentions divide by zero somewhere
    assert "Cannot divide by zero" in str(body)

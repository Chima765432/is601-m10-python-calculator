import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize("path, a, b, expected", [
    ("/add", -4, 1.5, -2.5),
    ("/subtract", 0.5, 0.25, 0.25),
    ("/multiply", -3, -3, 9),
    ("/divide", 7, 2, 3.5),
])
def test_endpoints_handle_negatives_and_decimals(path, a, b, expected):
    response = client.post(path, json={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(expected)


@pytest.mark.parametrize("payload, field", [
    ({"b": 2}, "a"),
    ({"a": 2}, "b"),
    ({"a": "two", "b": 2}, "a"),
    ({"a": 2, "b": None}, "b"),
])
def test_invalid_input_returns_400_naming_the_field(payload, field):
    response = client.post("/multiply", json=payload)
    assert response.status_code == 400
    assert response.json()["error"].startswith(f"{field}:")


def test_get_on_an_operation_is_not_allowed():
    assert client.get("/add").status_code == 405


def test_home_page_serves_the_calculator():
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="result"' in response.text


def test_health_endpoint_reports_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

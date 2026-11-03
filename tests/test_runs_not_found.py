"""坏路径：查不存在的工单，期望 404。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_run_not_found():
    response = client.get("/runs/999999")
    assert response.status_code == 404

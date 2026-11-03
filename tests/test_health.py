"""第一条项目用例：GET /health（骨架，由 Jonh 填写断言）。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
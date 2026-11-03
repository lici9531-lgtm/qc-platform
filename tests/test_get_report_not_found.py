"""坏路径：报告接口，工单不存在 → 404。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_report_not_found():
    # TODO: GET /runs/999999/report
    # TODO: assert status_code == 404
    pass
    response = client.get("/runs/999999/report")
    assert response.status_code == 404
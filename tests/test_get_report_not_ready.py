"""坏路径：工单 failed 时取报告 → 409。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_report_not_ready():
    # TODO: POST /datasets，file_path 用肯定不存在的路径，如 /tmp/no_such_qc_file.csv
    # TODO: POST /runs，拿到 run_id；可选 assert status == "failed"
    # TODO: GET /runs/{run_id}/report
    # TODO: assert status_code == 409
    pass
    response = client.post("/datasets", json={"name": "t1", "file_path": "/tmp/no_such_qc_file.csv"})
    dataset_id = response.json()["id"]
    response = client.post("/runs", json={"dataset_id": dataset_id})
    run_id = response.json()["id"]
    assert response.json()["status"] == "failed"
    response = client.get(f"/runs/{run_id}/report")
    assert response.status_code == 409
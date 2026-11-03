"""成功路径：开单成功后 GET /runs/{id}/report。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CSV = "/home/hanxi/Desktop/学习规划/05_代码与项目/练习/unit02/labels_okbad.csv"


def test_get_report_succeeded():
    # TODO: POST /datasets（真实 CSV）→ 取 dataset_id
    # TODO: POST /runs → 取 run_id
    # TODO: GET /runs/{run_id}/report
    # TODO: assert 200
    # TODO: assert "rules_version" in response.json()
    pass
    response = client.post("/datasets", json={"name": "t1", "file_path": CSV})
    dataset_id = response.json()["id"]
    response = client.post("/runs", json={"dataset_id": dataset_id})
    run_id = response.json()["id"]
    response = client.get(f"/runs/{run_id}/report")
    assert response.status_code == 200
    assert "rules_version" in response.json()

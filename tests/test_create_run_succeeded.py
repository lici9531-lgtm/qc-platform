"""成功路径：真实 CSV → 建档案 → 开单 → status=succeeded。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CSV = "/home/hanxi/Desktop/学习规划/05_代码与项目/练习/unit02/labels_okbad.csv"


def test_create_run_succeeded():
    # TODO: POST /datasets，json 用上面的 CSV 路径
    # TODO: 取出返回的 dataset id
    # TODO: POST /runs，json={"dataset_id": 那个 id}
    # TODO: assert 状态码 200
    # TODO: assert response.json()["status"] == "succeeded"
    pass
    response = client.post("/datasets", json={"name": "t1", "file_path": CSV})
    dataset_id = response.json()["id"]
    response = client.post("/runs", json={"dataset_id": dataset_id})
    assert response.status_code == 200
    assert response.json()["status"] == "succeeded"
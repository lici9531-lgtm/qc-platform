"""GET /runs 筛选、分页、参数校验。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CSV = "/home/hanxi/Desktop/学习规划/05_代码与项目/练习/unit02/labels_okbad.csv"


def test_list_runs_filter_by_dataset():
    # TODO: POST /datasets 用 CSV → 取 dataset_id
    # TODO: POST /runs 两次（同一个 dataset_id）
    # TODO: GET /runs，params={"dataset_id": dataset_id}
    # TODO: assert total == 2
    # TODO: assert 每个 item 的 dataset_id 都等于它（用 for 循环）
    dataset = client.post("/datasets", json={"name": "test_list_runs_filter_by_dataset", "description": "test_list_runs_filter_by_dataset", "file_path": CSV})
    dataset_id = dataset.json()["id"]
    run1 = client.post("/runs", json={"dataset_id": dataset_id, "name": "run1", "description": "run1"})
    run2 = client.post("/runs", json={"dataset_id": dataset_id, "name": "run2", "description": "run2"})
    runs = client.get("/runs", params={"dataset_id": dataset_id})
    assert runs.json()["total"] == 2
    for item in runs.json()["items"]:
        assert item["dataset_id"] == dataset_id


def test_list_runs_pagination():
    # TODO: 同上造 1 个 dataset + 2 个 run，记下第二个 run 的 id
    # TODO: GET /runs，params 带 dataset_id、limit=1、offset=1
    # TODO: assert items 长度 == 1，total == 2
    # TODO: assert items[0]["id"] == 第二个 run 的 id
    dataset = client.post("/datasets", json ={"name": "test_list_runs_pagination", "description": "test_list_runs_pagination", "file_path": CSV})
    dataset_id = dataset.json()["id"]
    run1 = client.post("/runs", json={"dataset_id": dataset_id, "name": "run1", "description": "run1"})
    run2 = client.post("/runs", json={"dataset_id": dataset_id, "name": "run2", "description": "run2"})
    run2_id = run2.json()["id"]
    runs = client.get("/runs", params={"dataset_id": dataset_id, "limit": 1, "offset": 1})
    assert runs.json()["total"] == 2
    assert len(runs.json()["items"]) == 1
    assert runs.json()["items"][0]["dataset_id"] == dataset_id
    assert runs.json()["items"][0]["id"] == run2_id


def test_list_runs_bad_params():
    # TODO: GET /runs?limit=51 → assert 422
    # TODO: GET /runs?status=abc → assert 422
    response = client.get("/runs", params={"limit": 51})
    assert response.status_code == 422
    response = client.get("/runs", params={"status": "abc"})
    assert response.status_code == 422

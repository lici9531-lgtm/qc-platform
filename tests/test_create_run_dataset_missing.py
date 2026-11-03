"""坏路径：POST /runs 时 dataset_id 不存在 → 404。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_run_dataset_not_found():
    # TODO: POST /runs，json={"dataset_id": 999999}
    # TODO: assert status_code == 404
    pass
    response = client.post("/runs", json={"dataset_id": 999999})
    assert response.status_code == 404
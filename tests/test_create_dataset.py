"""成功路径：POST /datasets 登记一条档案。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_dataset():
    # TODO: POST /datasets，json 含 name 与 file_path
    # TODO: assert 状态码 == 200
    # TODO: assert file_path 与传入一致
    # TODO: assert id 是 int
    pass
    response = client.post("/datasets", json={"name": "t1", "file_path": "/tmp/demo.csv"},
    )
    assert response.status_code == 200
    assert response.json()["file_path"] == "/tmp/demo.csv"
    assert isinstance(response.json()["id"], int)
from fastapi.testclient import TestClient

from .api.param.base import Result
from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/api/user/100000000")
    assert response.status_code == 200
    assert Result(**response.json()).code == 0
from starlette.testclient import TestClient
from requests import Response
from main import app

client = TestClient(app)


def test_health_check():
    prefix: str = '/api/v1'
    url: str = f"{prefix}/health-check"
    response: Response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {'message': 'alive!!!'}


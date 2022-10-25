import ulid
import json
from fastapi.testclient import TestClient
from fastapi import Response
from main import app

client = TestClient(app)


def test_signup():
    prefix: str = '/api/v1'
    url: str = f"{prefix}/accounts/signup"
    request_body: dict = {
        'email': f"{ulid.new().str}@example.come",
        'password': 'hogeH0g=',
        'password_confirmation': 'hogeH0g=',
    }

    client.headers["Content-Type"] = "application/json"
    response: Response = client.post(url, data=json.dumps(request_body))
    assert response.status_code == 201

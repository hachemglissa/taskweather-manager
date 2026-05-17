from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks?title=test&city=Tunis")
    assert response.status_code == 200
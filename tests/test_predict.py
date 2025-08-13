import base64
import numpy as np
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import app.services.model as model_service

client = TestClient(app)

def auth_header(u: str, p: str):
    token = base64.b64encode(f"{u}:{p}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

class EchoShapeModel:
    def predict(self, X):
        # Return the number of columns to prove we built a full frame
        return np.array([X.shape[1]], dtype=float)

def test_predict_partial_record(monkeypatch):
    settings.basic_auth_username = "user"
    settings.basic_auth_password = "pass"
    monkeypatch.setattr(model_service, "load_model", lambda: EchoShapeModel())

    headers = auth_header("user", "pass")
    # Only supply some fields; adapter should build 25 columns
    r = client.post("/v1/predict", json={"record": {"CarName": "toyota corolla", "enginesize": 130}}, headers=headers)
    assert r.status_code == 200
    assert r.json()["prediction"] == [25.0]

def test_predict_bad_length(monkeypatch):
    settings.basic_auth_username = "user"
    settings.basic_auth_password = "pass"
    monkeypatch.setattr(model_service, "load_model", lambda: EchoShapeModel())

    headers = auth_header("user", "pass")
    r = client.post("/v1/predict", json={"features":[1,2,3,4,5]}, headers=headers)
    assert r.status_code == 422
    assert "Expected 25 features" in r.json()["detail"]

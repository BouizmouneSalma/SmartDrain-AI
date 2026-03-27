import importlib
import sys
import types

import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.services.history_service import HistoryService
from app.models.user import User
from app.services.auth_service import AuthService


def _load_predict_module_with_fake_yolo(monkeypatch):
    class FakeBox:
        def __init__(self, cls_id: int, confidence: float, bbox: list[float]):
            self.cls = np.array([cls_id])
            self.conf = np.array([confidence])
            self.xyxy = np.array([bbox], dtype=float)

    class FakeResult:
        def __init__(self):
            self.names = {0: "lose", 1: "uncovered"}
            self.boxes = [
                FakeBox(0, 0.80, [10, 10, 120, 120]),
                FakeBox(1, 0.75, [20, 20, 130, 130]),
            ]

    class FakeYOLO:
        def __init__(self, _model_path: str):
            self.names = {0: "lose", 1: "uncovered"}

        def predict(self, *_args, **_kwargs):
            return [FakeResult()]

    fake_ultralytics = types.SimpleNamespace(YOLO=FakeYOLO)
    monkeypatch.setitem(sys.modules, "ultralytics", fake_ultralytics)
    sys.modules.pop("app.api.routes.predict", None)
    return importlib.import_module("app.api.routes.predict")


def _build_client(predict_module, db_session):
    app = FastAPI()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.include_router(predict_module.router)
    return TestClient(app)


def _seed_user(db_session, user_id: int = 1) -> None:
    existing = db_session.query(User).filter(User.id == user_id).first()
    if existing:
        return

    user = User(
        id=user_id,
        email=f"predict{user_id}@test.com",
        password_hash=AuthService._hash_password("secret123"),
    )
    db_session.add(user)
    db_session.commit()


def test_predict_image_invalid_file_returns_empty(monkeypatch, db_session):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)
    _seed_user(db_session, user_id=1)
    token = AuthService.create_access_token(1)

    with _build_client(predict_module, db_session) as client:
        response = client.post(
            "/predict/image",
            files={"file": ("not-image.txt", b"plain-text", "text/plain")},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["detections"] == []
    assert data["primary_detection"] is None


def test_predict_image_final_decision_overlap_to_broken(monkeypatch, db_session):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)
    _seed_user(db_session, user_id=1)
    token = AuthService.create_access_token(1)

    image = np.zeros((64, 64, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".jpg", image)
    assert ok

    with _build_client(predict_module, db_session) as client:
        response = client.post(
            "/predict/image?enhance=false",
            files={"file": ("image.jpg", encoded.tobytes(), "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["detections"]) == 2
    assert data["final_decision"]["label"] == "Broken"
    assert data["final_decision"]["reason"] == "lose_uncovered_overlap"

    history = HistoryService.list_history(db_session, user_id=1)
    assert len(history) == 1
    assert history[0]["filename"] == "image.jpg"
    assert history[0]["status"] == "Broken"
    assert history[0]["detectionCount"] == 2
    assert history[0]["type"] == "image"


def test_predict_history_isolated_by_user(monkeypatch, db_session):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)
    _seed_user(db_session, user_id=1)
    _seed_user(db_session, user_id=2)
    token_user_1 = AuthService.create_access_token(1)
    token_user_2 = AuthService.create_access_token(2)

    image = np.zeros((32, 32, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".jpg", image)
    assert ok

    with _build_client(predict_module, db_session) as client:
        client.post(
            "/predict/image?enhance=false",
            files={"file": ("u1.jpg", encoded.tobytes(), "image/jpeg")},
            headers={"Authorization": f"Bearer {token_user_1}"},
        )
        client.post(
            "/predict/image?enhance=false",
            files={"file": ("u2.jpg", encoded.tobytes(), "image/jpeg")},
            headers={"Authorization": f"Bearer {token_user_2}"},
        )

    history_user_1 = HistoryService.list_history(db_session, user_id=1)
    history_user_2 = HistoryService.list_history(db_session, user_id=2)
    assert len(history_user_1) == 1
    assert len(history_user_2) == 1
    assert history_user_1[0]["filename"] == "u1.jpg"
    assert history_user_2[0]["filename"] == "u2.jpg"


def test_resolve_final_decision_prefers_direct_broken(monkeypatch):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)

    detections = [
        {"class_name": "Good", "confidence": 0.95, "bbox": [0, 0, 10, 10]},
        {"class_name": "Broken", "confidence": 0.41, "bbox": [0, 0, 10, 10]},
    ]

    final = predict_module.resolve_final_decision(detections)

    assert final is not None
    assert final["label"] == "Broken"
    assert final["reason"] == "direct_broken_detection"

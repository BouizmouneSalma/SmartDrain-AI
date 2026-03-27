import importlib
import sys
import types

import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.testclient import TestClient


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


def test_predict_image_invalid_file_returns_empty(monkeypatch):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)

    app = FastAPI()
    app.include_router(predict_module.router)

    with TestClient(app) as client:
        response = client.post(
            "/predict/image",
            files={"file": ("not-image.txt", b"plain-text", "text/plain")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["detections"] == []
    assert data["primary_detection"] is None


def test_predict_image_final_decision_overlap_to_broken(monkeypatch):
    predict_module = _load_predict_module_with_fake_yolo(monkeypatch)

    app = FastAPI()
    app.include_router(predict_module.router)

    image = np.zeros((64, 64, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".jpg", image)
    assert ok

    with TestClient(app) as client:
        response = client.post(
            "/predict/image?enhance=false",
            files={"file": ("image.jpg", encoded.tobytes(), "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["detections"]) == 2
    assert data["final_decision"]["label"] == "Broken"
    assert data["final_decision"]["reason"] == "lose_uncovered_overlap"


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

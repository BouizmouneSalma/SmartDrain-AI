import os

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from ultralytics import YOLO

from app.core.database import get_db
from app.schemas.history import HistoryCreate
from app.services.history_service import HistoryService

router = APIRouter(prefix="/predict", tags=["Predict"])

DEFAULT_MODEL_PATH = "/app/ml/models/yolov8_cover-detector/weights/best.pt"
model = YOLO(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))

CLASS_ALIASES = {
    "broken": "Broken",
    "good": "Good",
    "lose": "Lose",
    "uncovered": "Uncovered",
}


def normalize_class_name(name: str) -> str:
    key = str(name).strip().lower()
    return CLASS_ALIASES.get(key, str(name).strip().title())


def enhance_image(image_bgr: np.ndarray) -> np.ndarray:
    # CLAHE enhances local contrast and often stabilizes detections in harsh lighting.
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l_channel)
    merged = cv2.merge((l_enhanced, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def rank_detection(det: dict) -> float:
    # Small prior on classes to reduce common confusion between similar classes.
    class_prior = {
        "Broken": 1.05,
        "Good": 1.0,
        "Lose": 1.0,
        "Uncovered": 1.02,
    }
    return det["confidence"] * class_prior.get(det["class_name"], 1.0)


def bbox_iou(box_a: list[float], box_b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0.0, (ax2 - ax1)) * max(0.0, (ay2 - ay1))
    area_b = max(0.0, (bx2 - bx1)) * max(0.0, (by2 - by1))
    union = area_a + area_b - inter_area

    if union <= 0:
        return 0.0
    return inter_area / union


def resolve_final_decision(detections: list[dict]) -> dict | None:
    if not detections:
        return None

    ranked = sorted(detections, key=rank_detection, reverse=True)

    broken = [d for d in detections if d["class_name"] == "Broken"]
    lose = [d for d in detections if d["class_name"] == "Lose"]
    uncovered = [d for d in detections if d["class_name"] == "Uncovered"]

    # If model already predicts Broken with solid confidence, keep it.
    if broken and broken[0]["confidence"] >= 0.40:
        top = sorted(broken, key=lambda d: d["confidence"], reverse=True)[0]
        return {
            "label": "Broken",
            "confidence": top["confidence"],
            "reason": "direct_broken_detection",
        }

    # Business rule: Lose + Uncovered overlap usually indicates a broken cover area.
    best_pair_iou = 0.0
    best_pair_conf = 0.0
    for l_det in lose:
        for u_det in uncovered:
            pair_iou = bbox_iou(l_det["bbox"], u_det["bbox"])
            pair_conf = min(l_det["confidence"], u_det["confidence"])
            if pair_iou > best_pair_iou:
                best_pair_iou = pair_iou
                best_pair_conf = pair_conf

    if best_pair_iou >= 0.22 and best_pair_conf >= 0.45:
        return {
            "label": "Broken",
            "confidence": best_pair_conf,
            "reason": "lose_uncovered_overlap",
            "overlap_iou": best_pair_iou,
        }

    top = ranked[0]
    return {
        "label": top["class_name"],
        "confidence": top["confidence"],
        "reason": "top_ranked_detection",
    }

@router.post("/image")
async def predict_image(
    file: UploadFile = File(...),
    conf: float = Query(default=0.25, ge=0.01, le=1.0),
    iou: float = Query(default=0.45, ge=0.1, le=0.95),
    imgsz: int = Query(default=1024, ge=320, le=1920),
    augment: bool = Query(default=True),
    enhance: bool = Query(default=True),
    max_det: int = Query(default=20, ge=1, le=300),
    db: Session = Depends(get_db),
):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {"detections": [], "model_classes": model.names, "primary_detection": None}

    if enhance:
        img = enhance_image(img)

    results = model.predict(
        img,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        augment=augment,
        max_det=max_det,
        verbose=False,
    )

    detections = []
    names = model.names

    for r in results:
        names = getattr(r, "names", model.names)
        for box in r.boxes:
            class_id = int(box.cls[0])
            if isinstance(names, dict):
                class_name = names.get(class_id, str(class_id))
            elif isinstance(names, list) and 0 <= class_id < len(names):
                class_name = names[class_id]
            else:
                class_name = str(class_id)

            detections.append({
                "class": class_id,
                "class_name": normalize_class_name(class_name),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    detections.sort(key=lambda d: d["confidence"], reverse=True)
    primary_detection = None
    if detections:
        primary_detection = sorted(detections, key=rank_detection, reverse=True)[0]

    final_decision = resolve_final_decision(detections)

    HistoryService.add_history(
        db,
        HistoryCreate(
            filename=file.filename or "uploaded_image",
            status=final_decision["label"] if final_decision else "NoDetection",
            detectionCount=len(detections),
            type="image",
        ),
    )

    return {
        "detections": detections,
        "primary_detection": primary_detection,
        "final_decision": final_decision,
        "model_classes": names,
        "inference": {
            "conf": conf,
            "iou": iou,
            "imgsz": imgsz,
            "augment": augment,
            "enhance": enhance,
            "max_det": max_det,
        },
    }


@router.post("/video")
async def predict_video(file: UploadFile = File(...)):
    return {"message": "Video prediction coming soon 🚧"}
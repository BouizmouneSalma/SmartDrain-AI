#route predict

from fastapi import APIRouter, UploadFile, File, Query
import cv2
import numpy as np
import os
from ultralytics import YOLO

router = APIRouter(prefix="/predict", tags=["Predict"])

DEFAULT_MODEL_PATH = "/app/ml/models/yolov8_cover-detector/weights/best.pt"
model = YOLO(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))

@router.post("/image")
async def predict_image(
    file: UploadFile = File(...),
    conf: float = Query(default=0.25, ge=0.01, le=1.0),
):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model.predict(img, conf=conf)

    detections = []

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
                "class_name": class_name,
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    detections.sort(key=lambda d: d["confidence"], reverse=True)
    return {"detections": detections, "model_classes": names}


@router.post("/video")
async def predict_video(file: UploadFile = File(...)):
    return {"message": "Video prediction coming soon 🚧"}
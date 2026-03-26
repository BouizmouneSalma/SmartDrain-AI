#route predict

from fastapi import APIRouter, UploadFile, File
import cv2
import numpy as np
import os
from ultralytics import YOLO

router = APIRouter(prefix="/predict", tags=["Predict"])

DEFAULT_MODEL_PATH = "/app/ml/models/yolov8_cover-detector/weights/best.pt"
model = YOLO(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))

@router.post("/image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model.predict(img, conf=0.25)

    detections = []

    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    return {"detections": detections}


@router.post("/video")
async def predict_video(file: UploadFile = File(...)):
    return {"message": "Video prediction coming soon 🚧"}
from ultralytics import YOLO

# Training entrypoint to improve detection quality on confusing classes.
# Run with: python ml/train_cover_detector.py

def main() -> None:
    model = YOLO("yolov8s.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=150,
        imgsz=1024,
        batch=8,
        patience=30,
        device=0,
        workers=4,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,
        cos_lr=True,
        weight_decay=0.0005,
        warmup_epochs=3,
        close_mosaic=10,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=5.0,
        translate=0.1,
        scale=0.4,
        shear=2.0,
        perspective=0.0005,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.1,
        copy_paste=0.0,
        project="ml/models",
        name="yolov8_cover-detector-v2",
        exist_ok=True,
        plots=True,
        verbose=True,
    )


if __name__ == "__main__":
    main()

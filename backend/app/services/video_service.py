import json
import os
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

OUTPUT_DIR = Path("/app/outputs") if os.path.exists("/app") else Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class VideoService:
    def __init__(self, model: YOLO):
        self.model = model

    @staticmethod
    def normalize_class_name(name: str) -> str:
        CLASS_ALIASES = {
            "broken": "Broken",
            "good": "Good",
            "lose": "Lose",
            "uncovered": "Uncovered",
        }
        key = str(name).strip().lower()
        return CLASS_ALIASES.get(key, str(name).strip().title())

    @staticmethod
    def enhance_image(image_bgr: np.ndarray) -> np.ndarray:
        """Apply CLAHE enhancement for better detection in harsh lighting."""
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l_channel)
        merged = cv2.merge((l_enhanced, a_channel, b_channel))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    @staticmethod
    def bbox_iou(box_a: list[float], box_b: list[float]) -> float:
        """Calculate Intersection over Union between two bounding boxes."""
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

    @staticmethod
    def rank_detection(det: dict) -> float:
        """Score detections with class-based priors."""
        class_prior = {
            "Broken": 1.05,
            "Good": 1.0,
            "Lose": 1.0,
            "Uncovered": 1.02,
        }
        return det["confidence"] * class_prior.get(det["class_name"], 1.0)

    def resolve_final_decision(self, detections: list[dict]) -> dict | None:
        """Business logic to resolve final decision from detections."""
        if not detections:
            return None

        ranked = sorted(detections, key=self.rank_detection, reverse=True)

        broken = [d for d in detections if d["class_name"] == "Broken"]
        lose = [d for d in detections if d["class_name"] == "Lose"]
        uncovered = [d for d in detections if d["class_name"] == "Uncovered"]

        # If model predicts Broken with solid confidence, keep it
        if broken and broken[0]["confidence"] >= 0.40:
            top = sorted(broken, key=lambda d: d["confidence"], reverse=True)[0]
            return {
                "label": "Broken",
                "confidence": top["confidence"],
                "reason": "direct_broken_detection",
            }

        # Business rule: Lose + Uncovered overlap usually indicates broken cover
        best_pair_iou = 0.0
        best_pair_conf = 0.0
        for l_det in lose:
            for u_det in uncovered:
                pair_iou = self.bbox_iou(l_det["bbox"], u_det["bbox"])
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

    def process_video(
        self,
        video_content: bytes,
        filename: str,
        conf: float = 0.25,
        iou: float = 0.45,
        imgsz: int = 1024,
        augment: bool = True,
        enhance: bool = True,
        max_det: int = 20,
    ) -> dict:
        """
        Process video: detect objects per frame, annotate, save output video.
        
        Returns:
            {
                "status": "success",
                "output_video": "path/to/output.mp4",
                "output_json": "path/to/output.json",
                "total_frames": int,
                "fps": float,
                "resolution": [width, height],
                "avg_detections_per_frame": float,
                "frame_results": [{frame_idx, detections, final_decision}, ...],
                "unique_classes_detected": [str],
            }
        """
        
        # Save temp input video
        temp_input_path = OUTPUT_DIR / f"temp_{datetime.now().timestamp()}.mp4"
        with open(temp_input_path, "wb") as f:
            f.write(video_content)

        # Open video
        cap = cv2.VideoCapture(str(temp_input_path))
        if not cap.isOpened():
            return {"status": "error", "message": "Failed to open video file"}

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Prepare output video writer
        output_filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_video_path = OUTPUT_DIR / output_filename
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

        # Color map for classes
        color_map = {
            "Broken": (0, 0, 255),      # Red
            "Good": (0, 255, 0),        # Green
            "Lose": (0, 165, 255),      # Orange
            "Uncovered": (255, 0, 0),   # Blue
        }

        frame_results = []
        all_classes = set()
        total_detections = 0
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Enhance if requested
            if enhance:
                frame = self.enhance_image(frame)

            # Run YOLO inference
            results = self.model.predict(
                frame,
                conf=conf,
                iou=iou,
                imgsz=imgsz,
                augment=augment,
                max_det=max_det,
                verbose=False,
            )

            # Extract detections
            detections = []
            names = self.model.names

            for r in results:
                names = getattr(r, "names", self.model.names)
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    if isinstance(names, dict):
                        class_name = names.get(class_id, str(class_id))
                    elif isinstance(names, list) and 0 <= class_id < len(names):
                        class_name = names[class_id]
                    else:
                        class_name = str(class_id)

                    normalized_class = self.normalize_class_name(class_name)
                    detections.append({
                        "class": class_id,
                        "class_name": normalized_class,
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist(),
                    })
                    all_classes.add(normalized_class)

            detections.sort(key=lambda d: d["confidence"], reverse=True)
            final_decision = self.resolve_final_decision(detections)
            total_detections += len(detections)

            # Draw bounding boxes on frame
            annotated_frame = frame.copy()
            for det in detections:
                x1, y1, x2, y2 = det["bbox"]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                class_name = det["class_name"]
                confidence = det["confidence"]
                
                # Get color
                color = color_map.get(class_name, (255, 255, 255))
                
                # Draw box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} {confidence:.2f}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                (text_width, text_height) = cv2.getTextSize(label, font, font_scale, thickness)[0]
                
                text_bg_x1 = x1
                text_bg_y1 = y1 - text_height - 5
                text_bg_x2 = x1 + text_width
                text_bg_y2 = y1
                
                cv2.rectangle(annotated_frame, (text_bg_x1, text_bg_y1), (text_bg_x2, text_bg_y2), color, -1)
                cv2.putText(annotated_frame, label, (x1, y1 - 5), font, font_scale, (255, 255, 255), thickness)

            # Write annotated frame to output video
            out.write(annotated_frame)

            # Store frame results
            frame_results.append({
                "frame_idx": frame_idx,
                "detections": detections,
                "final_decision": final_decision,
            })

            frame_idx += 1

        cap.release()
        out.release()

        # Save JSON results
        output_json_filename = output_filename.replace(".mp4", ".json")
        output_json_path = OUTPUT_DIR / output_json_filename
        
        with open(output_json_path, "w") as f:
            json.dump({
                "filename": filename,
                "output_video": str(output_video_path),
                "total_frames": total_frames,
                "fps": fps,
                "resolution": [width, height],
                "processing_params": {
                    "conf": conf,
                    "iou": iou,
                    "imgsz": imgsz,
                    "augment": augment,
                    "enhance": enhance,
                    "max_det": max_det,
                },
                "unique_classes_detected": sorted(list(all_classes)),
                "total_detections": total_detections,
                "frame_results": frame_results,
            }, f, indent=2)

        # Cleanup temp file
        os.remove(temp_input_path)

        return {
            "status": "success",
            "output_video": str(output_video_path),
            "output_json": str(output_json_path),
            "total_frames": total_frames,
            "fps": fps,
            "resolution": [width, height],
            "avg_detections_per_frame": total_detections / total_frames if total_frames > 0 else 0,
            "frame_results": frame_results,
            "unique_classes_detected": sorted(list(all_classes)),
            "total_detections": total_detections,
        }

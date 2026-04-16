from __future__ import annotations

from typing import Any, Dict

from PIL import Image

from src.aggregation import summarize_faces
from src.config import FAKE_SCORE_THRESHOLD
from src.face_service import FaceDetector
from src.model_service import DeepFakeModelService
from src.rendering import draw_boxes_on_image


def process_image(
    image: Image.Image,
    face_detector: FaceDetector,
    model_service: DeepFakeModelService,
    fake_score_threshold: float = FAKE_SCORE_THRESHOLD,
    invert_labels: bool = False,
) -> Dict[str, Any]:
    rgb_image = image.convert("RGB")
    detections = face_detector.detect(rgb_image)

    if not detections:
        summary = summarize_faces([], fake_score_threshold=fake_score_threshold)
        return {
            "annotated_image": rgb_image,
            "summary": summary,
            "faces": [],
        }

    face_results = []
    for detection in detections:
        prediction = model_service.predict(detection.crop, invert_labels=invert_labels)
        face_results.append(
            {
                "bbox": detection.bbox,
                "face_confidence": round(detection.confidence, 6),
                "predicted_label": prediction.predicted_label,
                "label_confidence": round(prediction.label_confidence, 6),
                "deepfake_probability": round(prediction.deepfake_probability, 6),
                "realism_probability": round(prediction.realism_probability, 6),
            }
        )

    summary = summarize_faces(face_results, fake_score_threshold=fake_score_threshold)
    annotated = draw_boxes_on_image(
        image=rgb_image,
        face_results=face_results,
        fake_score_threshold=fake_score_threshold,
    )

    return {
        "annotated_image": annotated,
        "summary": summary,
        "faces": face_results,
    }

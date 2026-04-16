from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List

from src.config import FAKE_SCORE_THRESHOLD, NO_FACE_MESSAGE


def summarize_faces(
    face_predictions: List[Dict[str, Any]],
    fake_score_threshold: float = FAKE_SCORE_THRESHOLD,
) -> Dict[str, Any]:
    if not face_predictions:
        return {
            "status": "no_face_detected",
            "overall_label": NO_FACE_MESSAGE,
            "message": NO_FACE_MESSAGE,
            "total_faces": 0,
            "fake_faces": 0,
            "max_deepfake_probability": 0.0,
            "average_deepfake_probability": 0.0,
        }

    deepfake_scores = [float(item["deepfake_probability"]) for item in face_predictions]
    fake_faces = sum(score >= fake_score_threshold for score in deepfake_scores)
    max_score = max(deepfake_scores)

    overall_label = "Deepfake" if max_score >= fake_score_threshold else "Realism"

    return {
        "status": "ok",
        "overall_label": overall_label,
        "total_faces": len(face_predictions),
        "fake_faces": fake_faces,
        "fake_ratio": round(fake_faces / len(face_predictions), 4),
        "max_deepfake_probability": round(max_score, 6),
        "average_deepfake_probability": round(mean(deepfake_scores), 6),
        "decision_threshold": fake_score_threshold,
    }


def summarize_video(
    all_face_predictions: List[Dict[str, Any]],
    sampled_frames: int,
    frames_with_faces: int,
    fake_score_threshold: float = FAKE_SCORE_THRESHOLD,
) -> Dict[str, Any]:
    base = summarize_faces(
        face_predictions=all_face_predictions,
        fake_score_threshold=fake_score_threshold,
    )

    base["sampled_frames"] = sampled_frames
    base["frames_with_faces"] = frames_with_faces

    if sampled_frames > 0:
        base["face_frame_ratio"] = round(frames_with_faces / sampled_frames, 4)
    else:
        base["face_frame_ratio"] = 0.0

    return base

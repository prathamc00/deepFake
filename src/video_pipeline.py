from __future__ import annotations

import os
import tempfile
from typing import Any, Dict, List

import cv2
import numpy as np
from PIL import Image

from src.aggregation import summarize_video
from src.config import FAKE_SCORE_THRESHOLD, MAX_VIDEO_FRAMES_TO_PROCESS, VIDEO_SAMPLE_RATE
from src.face_service import FaceDetector
from src.model_service import DeepFakeModelService
from src.rendering import draw_boxes_on_image


def _write_preview_video(frames: List[np.ndarray], fps: float) -> str:
    temp_dir = tempfile.mkdtemp(prefix="deepfake_preview_")
    preview_path = os.path.join(temp_dir, "annotated_preview.mp4")

    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(preview_path, fourcc, fps, (width, height))

    for frame in frames:
        writer.write(frame)

    writer.release()
    return preview_path


def process_video(
    video_path: str,
    face_detector: FaceDetector,
    model_service: DeepFakeModelService,
    sample_rate: int = VIDEO_SAMPLE_RATE,
    fake_score_threshold: float = FAKE_SCORE_THRESHOLD,
    max_frames_to_process: int = MAX_VIDEO_FRAMES_TO_PROCESS,
    invert_labels: bool = False,
) -> Dict[str, Any]:
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise ValueError("Unable to open video file.")

    original_fps = capture.get(cv2.CAP_PROP_FPS) or 24.0
    preview_fps = max(1.0, original_fps / max(1, sample_rate))

    frame_index = 0
    sampled_frames = 0
    processed_frames = 0
    frames_with_faces = 0

    all_face_results: List[Dict[str, Any]] = []
    preview_frames: List[np.ndarray] = []

    while True:
        ok, frame_bgr = capture.read()
        if not ok:
            break

        if frame_index % sample_rate != 0:
            frame_index += 1
            continue

        sampled_frames += 1
        processed_frames += 1

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)

        detections = face_detector.detect(frame_image)
        frame_face_results: List[Dict[str, Any]] = []

        for detection in detections:
            prediction = model_service.predict(detection.crop, invert_labels=invert_labels)
            face_result = {
                "frame_index": frame_index,
                "bbox": detection.bbox,
                "face_confidence": round(detection.confidence, 6),
                "predicted_label": prediction.predicted_label,
                "label_confidence": round(prediction.label_confidence, 6),
                "deepfake_probability": round(prediction.deepfake_probability, 6),
                "realism_probability": round(prediction.realism_probability, 6),
            }
            frame_face_results.append(face_result)
            all_face_results.append(face_result)

        if frame_face_results:
            frames_with_faces += 1

        annotated = draw_boxes_on_image(
            image=frame_image,
            face_results=frame_face_results,
            fake_score_threshold=fake_score_threshold,
        )
        annotated_bgr = cv2.cvtColor(np.array(annotated), cv2.COLOR_RGB2BGR)
        preview_frames.append(annotated_bgr)

        if processed_frames >= max_frames_to_process:
            break

        frame_index += 1

    capture.release()

    summary = summarize_video(
        all_face_predictions=all_face_results,
        sampled_frames=sampled_frames,
        frames_with_faces=frames_with_faces,
        fake_score_threshold=fake_score_threshold,
    )

    preview_video_path = None
    if preview_frames:
        preview_video_path = _write_preview_video(preview_frames, preview_fps)

    return {
        "preview_video_path": preview_video_path,
        "summary": summary,
        "faces": all_face_results,
    }

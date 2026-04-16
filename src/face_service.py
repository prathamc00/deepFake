from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from PIL import Image

from src.config import FACE_CONFIDENCE_THRESHOLD, MAX_FACES_PER_FRAME


@dataclass
class FaceDetection:
    bbox: Tuple[int, int, int, int]
    confidence: float
    crop: Image.Image


class FaceDetector:
    def __init__(
        self,
        confidence_threshold: float = FACE_CONFIDENCE_THRESHOLD,
        max_faces: int = MAX_FACES_PER_FRAME,
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.max_faces = max_faces
        self._device: Optional[Any] = None
        self._mtcnn: Optional[Any] = None

    def _ensure_loaded(self) -> None:
        if self._mtcnn is not None:
            return

        try:
            import torch
            from facenet_pytorch import MTCNN
        except Exception as exc:  # pragma: no cover - depends on local runtime
            raise RuntimeError(
                "Torch/MTCNN could not be imported. Install dependencies and ensure VC++ runtime is available."
            ) from exc

        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._mtcnn = MTCNN(
            keep_all=True,
            post_process=False,
            device=self._device,
        )

    def detect(self, image: Image.Image) -> List[FaceDetection]:
        self._ensure_loaded()
        assert self._mtcnn is not None

        boxes, probs = self._mtcnn.detect(image.convert("RGB"))
        if boxes is None or probs is None:
            return []

        width, height = image.size
        detections: List[FaceDetection] = []

        for box, prob in zip(boxes, probs):
            confidence = float(prob) if prob is not None else 0.0
            if confidence < self.confidence_threshold:
                continue

            x1, y1, x2, y2 = [int(round(value)) for value in box.tolist()]
            x1 = max(0, min(x1, width - 1))
            y1 = max(0, min(y1, height - 1))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))

            if x2 <= x1 or y2 <= y1:
                continue

            face_crop = image.crop((x1, y1, x2, y2)).convert("RGB")
            detections.append(
                FaceDetection(
                    bbox=(x1, y1, x2, y2),
                    confidence=confidence,
                    crop=face_crop,
                )
            )

        detections.sort(key=lambda item: item.confidence, reverse=True)
        return detections[: self.max_faces]

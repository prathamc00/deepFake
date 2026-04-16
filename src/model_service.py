from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from PIL import Image

from src.config import MODEL_NAME


@dataclass
class Prediction:
    predicted_label: str
    label_confidence: float
    deepfake_probability: float
    realism_probability: float


class DeepFakeModelService:
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.model_name = model_name
        self._model: Optional[Any] = None
        self._processor: Optional[Any] = None
        self._torch: Optional[Any] = None
        self._device: Optional[Any] = None
        self._deepfake_index: Optional[int] = None
        self._realism_index: Optional[int] = None

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._processor is not None:
            return

        try:
            import torch
            from transformers import ViTForImageClassification, ViTImageProcessor
        except Exception as exc:  # pragma: no cover - depends on local runtime
            raise RuntimeError(
                "PyTorch/Transformers could not be imported. Install dependencies and ensure VC++ runtime is available."
            ) from exc

        self._torch = torch
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._processor = ViTImageProcessor.from_pretrained(self.model_name)
        self._model = ViTForImageClassification.from_pretrained(self.model_name)
        self._model.to(self._device)
        self._model.eval()
        self._infer_label_indices()

    def _infer_label_indices(self) -> None:
        assert self._model is not None

        deepfake_index = None
        realism_index = None

        for idx, label in self._model.config.id2label.items():
            normalized = label.lower()
            if "deepfake" in normalized or normalized == "fake":
                deepfake_index = int(idx)
            if "real" in normalized:
                realism_index = int(idx)

        if deepfake_index is None and len(self._model.config.id2label) > 1:
            deepfake_index = 1
        if realism_index is None:
            realism_index = 0

        self._deepfake_index = deepfake_index
        self._realism_index = realism_index

    def predict(self, image: Image.Image, invert_labels: bool = False) -> Prediction:
        self._ensure_loaded()
        assert self._model is not None and self._processor is not None
        assert self._torch is not None
        assert self._deepfake_index is not None and self._realism_index is not None

        rgb_image = image.convert("RGB")
        inputs = self._processor(images=rgb_image, return_tensors="pt")
        inputs = {key: value.to(self._device) for key, value in inputs.items()}

        with self._torch.no_grad():
            logits = self._model(**inputs).logits
            probabilities = self._torch.softmax(logits, dim=-1).squeeze(0).detach().cpu().tolist()

        predicted_idx = int(self._torch.argmax(logits, dim=-1).item())
        predicted_label = self._model.config.id2label[predicted_idx]

        deepfake_probability = float(probabilities[self._deepfake_index])
        realism_probability = float(probabilities[self._realism_index])

        if invert_labels:
            deepfake_probability, realism_probability = realism_probability, deepfake_probability

        if deepfake_probability >= realism_probability:
            predicted_label = "Deepfake"
            label_confidence = deepfake_probability
        else:
            predicted_label = "Realism"
            label_confidence = realism_probability

        return Prediction(
            predicted_label=predicted_label,
            label_confidence=label_confidence,
            deepfake_probability=deepfake_probability,
            realism_probability=realism_probability,
        )

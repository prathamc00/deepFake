from PIL import Image

from src.image_pipeline import process_image


class DummyFace:
    def __init__(self, bbox, confidence, crop):
        self.bbox = bbox
        self.confidence = confidence
        self.crop = crop


class DummyFaceDetector:
    def detect(self, image):
        return []


class DummyModelService:
    def predict(self, image):
        raise RuntimeError("Should not be called when no face is detected.")


def test_process_image_returns_no_face_detected() -> None:
    image = Image.new("RGB", (100, 100), color=(120, 120, 120))
    result = process_image(
        image=image,
        face_detector=DummyFaceDetector(),
        model_service=DummyModelService(),
    )
    assert result["summary"]["status"] == "no_face_detected"
    assert result["summary"]["overall_label"] == "No face detected"
    assert result["faces"] == []

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw


def _label_text(face_result: Dict[str, Any]) -> str:
    label = str(face_result.get("predicted_label", "Unknown"))
    deepfake_prob = float(face_result.get("deepfake_probability", 0.0))
    return f"{label} | fake={deepfake_prob:.2f}"


def draw_boxes_on_image(
    image: Image.Image,
    face_results: List[Dict[str, Any]],
    fake_score_threshold: float,
) -> Image.Image:
    annotated = image.convert("RGB").copy()
    draw = ImageDraw.Draw(annotated)

    for face in face_results:
        x1, y1, x2, y2 = face["bbox"]
        deepfake_prob = float(face.get("deepfake_probability", 0.0))
        color: Tuple[int, int, int] = (220, 40, 40) if deepfake_prob >= fake_score_threshold else (34, 139, 34)

        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=3)

        text = _label_text(face)
        text_x = x1
        text_y = max(0, y1 - 14)
        draw.text((text_x, text_y), text, fill=color)

    return annotated

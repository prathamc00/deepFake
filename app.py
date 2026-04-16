from __future__ import annotations

import json
from typing import Any, Dict, Tuple

import gradio as gr
from PIL import Image

from src.config import FAKE_SCORE_THRESHOLD, VIDEO_SAMPLE_RATE
from src.face_service import FaceDetector
from src.image_pipeline import process_image
from src.model_service import DeepFakeModelService
from src.video_pipeline import process_video

model_service = DeepFakeModelService()
face_detector = FaceDetector()


def _build_payload(summary: Dict[str, Any], faces: list[Dict[str, Any]]) -> str:
    return json.dumps(
        {
            "summary": summary,
            "faces": faces,
        },
        indent=2,
    )


def run_image_detection(image: Image.Image, flip_labels: bool) -> Tuple[Image.Image | None, str]:
    if image is None:
        return None, _build_payload(
            summary={"status": "error", "message": "Please upload an image."},
            faces=[],
        )

    try:
        result = process_image(
            image=image,
            face_detector=face_detector,
            model_service=model_service,
            fake_score_threshold=FAKE_SCORE_THRESHOLD,
            invert_labels=flip_labels,
        )
        return result["annotated_image"], _build_payload(result["summary"], result["faces"])
    except Exception as exc:
        return None, _build_payload(
            summary={"status": "error", "message": str(exc)},
            faces=[],
        )


def run_video_detection(video_path: str, sample_rate: int, flip_labels: bool) -> Tuple[str | None, str]:
    if not video_path:
        return None, _build_payload(
            summary={"status": "error", "message": "Please upload a video."},
            faces=[],
        )

    try:
        result = process_video(
            video_path=video_path,
            face_detector=face_detector,
            model_service=model_service,
            sample_rate=max(1, int(sample_rate)),
            fake_score_threshold=FAKE_SCORE_THRESHOLD,
            invert_labels=flip_labels,
        )
        return result["preview_video_path"], _build_payload(result["summary"], result["faces"])
    except Exception as exc:
        return None, _build_payload(
            summary={"status": "error", "message": str(exc)},
            faces=[],
        )


CSS = """
.warning-banner {
    background: linear-gradient(90deg, #07213d, #0e3d66);
    border: 1px solid #12a8ff;
    color: #d9f2ff;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.4;
    margin-bottom: 16px;
}
.app-title {
    font-size: 28px;
    font-weight: 700;
    margin: 8px 0 14px;
}
"""


with gr.Blocks(title="Deepfake Detector") as demo:
    gr.HTML(
        """
        <div class='warning-banner'>
            AI model outputs can be inaccurate or biased. Do not use this tool as legal or forensic proof.
            Avoid uploading confidential or personal data unless you have permission.
        </div>
        <div class='app-title'>Deepfake Detection (Image + Video)</div>
        """
    )

    with gr.Tab("Image Detection"):
        image_input = gr.Image(type="pil", label="Upload image")
        image_flip = gr.Checkbox(label="Flip Real/Fake labels", value=False)
        image_button = gr.Button("Detect")
        image_output = gr.Image(type="pil", label="Annotated image")
        image_json = gr.Code(language="json", label="Detection details")
        image_button.click(
            fn=run_image_detection,
            inputs=[image_input, image_flip],
            outputs=[image_output, image_json],
        )

    with gr.Tab("Video Detection"):
        video_input = gr.Video(label="Upload video", sources=["upload"])
        sample_slider = gr.Slider(
            label="Frame sampling rate (process every Nth frame)",
            minimum=1,
            maximum=30,
            value=VIDEO_SAMPLE_RATE,
            step=1,
        )
        video_flip = gr.Checkbox(label="Flip Real/Fake labels", value=False)
        video_button = gr.Button("Detect")
        video_output = gr.Video(label="Annotated sampled frames preview")
        video_json = gr.Code(language="json", label="Detection details")
        video_button.click(
            fn=run_video_detection,
            inputs=[video_input, sample_slider, video_flip],
            outputs=[video_output, video_json],
        )


if __name__ == "__main__":
    demo.launch(css=CSS)

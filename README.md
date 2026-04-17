# Deepfake Detection App (Image + Video)

This project provides deepfake detection for images and videos using:

- Hugging Face model: `prithivMLmods/Deep-Fake-Detector-v2-Model`
- Face detection: MTCNN (`facenet-pytorch`)
- UI: Gradio

For videos, the app samples every Nth frame, detects faces, classifies each face, and aggregates one final verdict.

## Features

- Image deepfake detection with face bounding boxes
- Video deepfake detection with frame sampling
- Per-face predictions and overall verdict
- Explicit `No face detected` result when no valid faces are found
- Warning banner in UI for safe usage

## Project Structure

- `app.py`: Gradio app entrypoint
- `src/model_service.py`: model loading and inference
- `src/face_service.py`: MTCNN detection and face crops
- `src/image_pipeline.py`: image processing flow
- `src/video_pipeline.py`: sampled-frame video processing
- `src/rendering.py`: box rendering helpers
- `src/aggregation.py`: overall decision logic

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

Then open the local Gradio URL shown in the terminal.

## Notes

- The classifier is image-based. Video detection is an approximation through sampled frame analysis.
- First run downloads model weights, so startup can take longer.
- If you get codec issues on videos, install FFmpeg and retry.

## Tuning

You can tune defaults in `src/config.py`:

- `FACE_CONFIDENCE_THRESHOLD`
- `FAKE_SCORE_THRESHOLD`
- `VIDEO_SAMPLE_RATE`
- `MAX_FACES_PER_FRAME`
- `MAX_VIDEO_FRAMES_TO_PROCESS`

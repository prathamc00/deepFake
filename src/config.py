"""Configuration values for deepfake detector app."""

MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-v2-Model"

FACE_CONFIDENCE_THRESHOLD = 0.90
FAKE_SCORE_THRESHOLD = 0.50
MAX_FACES_PER_FRAME = 5

VIDEO_SAMPLE_RATE = 8
MAX_VIDEO_FRAMES_TO_PROCESS = 300

NO_FACE_MESSAGE = "No face detected"

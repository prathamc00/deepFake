from src.aggregation import summarize_faces


def test_summarize_faces_no_face_detected() -> None:
    summary = summarize_faces([])
    assert summary["status"] == "no_face_detected"
    assert summary["overall_label"] == "No face detected"


def test_summarize_faces_detects_deepfake_when_max_crosses_threshold() -> None:
    faces = [
        {"deepfake_probability": 0.21},
        {"deepfake_probability": 0.88},
    ]
    summary = summarize_faces(faces, fake_score_threshold=0.5)
    assert summary["overall_label"] == "Deepfake"
    assert summary["fake_faces"] == 1

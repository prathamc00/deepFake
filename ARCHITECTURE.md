# Deepfake Detection System Architecture

## 1. High-Level Architecture

```mermaid
flowchart TD
    U[User] --> UI[Gradio Web UI]

    UI --> IMG[Image Detection Tab]
    UI --> VID[Video Detection Tab]

    IMG --> I_PIPE[Image Pipeline]
    VID --> V_PIPE[Video Pipeline]

    I_PIPE --> FACE[Face Detection Service\nMTCNN]
    V_PIPE --> FACE

    FACE -->|No faces| NOFACE[No Face Handler]
    NOFACE --> SUM[Result Aggregator]

    FACE -->|Face crops + bbox| MODEL[Model Service\nViT Deepfake Classifier]

    MODEL --> I_PIPE
    MODEL --> V_PIPE

    I_PIPE --> RENDER[Rendering Service\nBounding Boxes + Labels]
    V_PIPE --> RENDER

    RENDER --> SUM
    SUM --> JSON[JSON Response Builder]

    JSON --> OUT1[Annotated Image / Video Preview]
    JSON --> OUT2[Summary + Per-Face Details]

    OUT1 --> UI
    OUT2 --> UI
```

## 2. Layered View

```mermaid
flowchart LR
    subgraph L1[Presentation Layer]
        A1[Gradio Blocks UI]
        A2[Image/Video Inputs]
        A3[Result Panels]
    end

    subgraph L2[Application Layer]
        B1[app.py Handlers]
        B2[Image Pipeline]
        B3[Video Pipeline]
        B4[Aggregation]
        B5[Rendering]
    end

    subgraph L3[ML Services Layer]
        C1[FaceDetector - MTCNN]
        C2[DeepFakeModelService - ViT]
    end

    subgraph L4[Media Processing Layer]
        D1[Pillow RGB Processing]
        D2[OpenCV Video Decode/Encode]
    end

    subgraph L5[Configuration Layer]
        E1[Thresholds]
        E2[Sampling Controls]
        E3[Runtime Parameters]
    end

    L1 --> L2 --> L3 --> L4
    L2 --> L5
```

## 3. Sequence (Image Request)

```mermaid
sequenceDiagram
    participant User
    participant UI as Gradio UI
    participant IP as Image Pipeline
    participant FD as FaceDetector (MTCNN)
    participant MS as ModelService (ViT)
    participant AG as Aggregator

    User->>UI: Upload image + click Detect
    UI->>IP: run_image_detection(image, options)
    IP->>FD: detect(image)
    FD-->>IP: detections / empty

    alt no face
        IP->>AG: summarize_faces([])
        AG-->>IP: no_face_detected summary
    else faces found
        loop each face
            IP->>MS: predict(face_crop)
            MS-->>IP: label + probabilities
        end
        IP->>AG: summarize_faces(face_predictions)
        AG-->>IP: overall verdict
    end

    IP-->>UI: annotated_image + JSON result
    UI-->>User: Display outputs
```

## 4. Sequence (Video Request)

```mermaid
sequenceDiagram
    participant User
    participant UI as Gradio UI
    participant VP as Video Pipeline
    participant FD as FaceDetector (MTCNN)
    participant MS as ModelService (ViT)
    participant AG as Aggregator

    User->>UI: Upload video + click Detect
    UI->>VP: run_video_detection(path, sample_rate, options)

    loop sampled frame
        VP->>FD: detect(frame)
        FD-->>VP: detections
        loop each face
            VP->>MS: predict(face_crop)
            MS-->>VP: label + probabilities
        end
    end

    VP->>AG: summarize_video(all_face_predictions)
    AG-->>VP: overall verdict + stats
    VP-->>UI: preview_video + JSON result
    UI-->>User: Display outputs
```

## 5. Component Responsibilities

- `app.py`: UI events, input validation, output packaging.
- `src/face_service.py`: face detection, bbox clipping, confidence filtering.
- `src/model_service.py`: lazy model load, inference, probability outputs.
- `src/image_pipeline.py`: single-image end-to-end flow.
- `src/video_pipeline.py`: sampled-frame video flow and preview build.
- `src/rendering.py`: draw labels and face boxes.
- `src/aggregation.py`: no-face handling and final decision logic.
- `src/config.py`: thresholds, sampling, and runtime constants.

## 6. Data Contracts

### Face Prediction Item

- `bbox`: [x1, y1, x2, y2]
- `face_confidence`: float
- `predicted_label`: string
- `label_confidence`: float
- `deepfake_probability`: float
- `realism_probability`: float

### Summary Object

- `status`: ok | no_face_detected | error
- `overall_label`: Deepfake | Realism | No face detected
- `total_faces`: int
- `fake_faces`: int
- `max_deepfake_probability`: float
- `average_deepfake_probability`: float

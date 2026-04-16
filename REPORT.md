# Deepfake Detection System Report

## Front Matter

### Title

Deepfake Detection for Images and Videos Using MTCNN Face Localization and Vision Transformer Classification

### Author Statement

I designed, implemented, and integrated this project as an end-to-end system for deepfake analysis in both image and video media. I trained the classification model pipeline on a dataset containing real and deepfake face images and then integrated model inference into a complete user-facing application.

### Abstract

The rapid advancement of generative artificial intelligence has made synthetic media creation easier, faster, and more realistic than ever before. Deepfake technology, while useful in film production, education, and content generation, also introduces significant risks related to misinformation, identity misuse, financial fraud, political manipulation, and digital trust erosion. This report presents a practical deepfake detection system built for real-world usability, with support for both static images and video files. The solution combines two major components: face detection and deepfake classification. For face detection and localization, the project uses Multi-task Cascaded Convolutional Neural Networks (MTCNN), enabling robust identification of facial regions and generation of face-level bounding boxes. For deepfake classification, the project uses a Vision Transformer (ViT)-based model integrated from a Hugging Face checkpoint and adapted into an operational inference pipeline.

The implemented application receives user-provided media, detects faces, performs classification on each face crop, and returns a detailed output including predicted label, confidence scores, deepfake probability, and an aggregated final verdict. A dedicated no-face branch ensures graceful handling of non-human content by returning an explicit "No face detected" status when no valid face is found. For video input, the system performs sampled-frame processing to balance computational cost and inference coverage. The interface layer is implemented using Gradio, offering separate workflows for image and video analysis and rendering annotated media outputs with visual overlays.

The report documents architecture, model assumptions, implementation details, dependency management, compatibility issues, debugging process, and evaluation strategy. It also discusses ethical and operational constraints, including domain shift, compression artifacts, and confidence calibration limitations. Beyond implementation, this report emphasizes reproducibility, maintainability, and practical deployment readiness. The resulting system demonstrates that a modular pipeline combining reliable face localization, transformer-based classification, robust fallback logic, and user-friendly interaction can provide a useful baseline for deepfake risk screening in applied settings.

### Keywords

Deepfake Detection, MTCNN, Vision Transformer, Face Classification, Media Forensics, Gradio, Video Analysis, Trust and Safety

---

## Table of Contents

1. Introduction
2. Problem Statement and Motivation
3. Objectives and Scope
4. Literature and Technical Background
5. System Requirements
6. Dataset and Training Detail
7. Proposed Architecture
8. Module-Wise Design
9. Implementation Details
10. Image Detection Workflow
11. Video Detection Workflow
12. Aggregation Strategy and Decision Logic
13. User Interface Design and Experience
14. Error Handling and Reliability Strategy
15. Environment and Dependency Engineering
16. Testing and Validation
17. Experimental Observations
18. Performance Discussion
19. Security, Ethics, and Responsible Use
20. Limitations
21. Future Work
22. Conclusion
23. References
24. Appendix A: Data Schemas
25. Appendix B: Key Functions and Pseudocode
26. Appendix C: Troubleshooting and Operations Guide

---

## 1. Introduction

Digital media has become central to communication, journalism, education, governance, and social interaction. As content generation systems become more capable, synthetic visual artifacts have shifted from obvious manipulations to highly realistic outputs that are difficult to distinguish from genuine recordings using casual human inspection. The concept of a deepfake traditionally refers to synthetic or manipulated content generated or altered using deep learning models, particularly in the domain of human faces, lip synchronization, identity replacement, and expression editing.

The social impact of deepfakes can be severe. In public discourse, manipulated clips can influence perception before verification catches up. In personal domains, identity abuse and harassment are increasing concerns. In enterprise and security contexts, spoofed media can damage trust in KYC workflows, social engineering defenses, and digital evidence validation. As a result, automated detection tools are increasingly needed not only for research but for operational pipelines where rapid triage is essential.

This project was developed as a practical engineering solution: a usable deepfake detector that supports both image and video input, highlights detected face regions, and returns interpretable confidence summaries. Rather than relying on opaque single-number output alone, this system was designed to provide per-face details, frame-level analysis for videos, and a clear fallback response for no-face scenarios. The goal is not to claim perfect forensic certainty but to deliver an actionable first-level detector for screening and review support.

This report presents the complete lifecycle of the project: planning, architecture, implementation, debugging, environment compatibility handling, evaluation, and limitations. Particular focus is given to robust software behavior under real user interaction, including corrupted input, absent faces, classifier orientation mismatch, and package compatibility constraints.

## 2. Problem Statement and Motivation

### 2.1 Problem Statement

The core problem addressed in this project is:

How can we build a practical, user-friendly deepfake detection application that supports both images and videos, localizes faces with bounding boxes, and provides reliable outputs including a clear no-face response?

This problem has technical, operational, and user-experience dimensions. A purely model-centric solution is insufficient if it cannot process realistic media formats, handle edge cases, or communicate confidence outputs clearly.

### 2.2 Motivation

The motivation behind this work includes:

- Need for a practical detector that non-expert users can run through a simple interface.
- Need for face-level interpretation instead of black-box whole-image decision only.
- Need for video support, since many harmful deepfakes circulate as clips rather than still images.
- Need for robust fallback paths to avoid misleading output when no faces are present.
- Need for maintainable, modular code suitable for further extension and deployment.

### 2.3 Practical Constraints

This project intentionally targets a realistic developer setup on consumer hardware and standard Python tooling. Therefore, the solution must work under CPU fallback, handle dependency conflicts, and avoid assumptions about high-end GPUs or proprietary inference infrastructure.

## 3. Objectives and Scope

### 3.1 Primary Objectives

The project objectives were:

1. Build an image deepfake detection pipeline with face localization.
2. Build a video deepfake detection pipeline using sampled frames.
3. Use MTCNN to generate face bounding boxes.
4. Integrate ViT classifier for face-level Realism/Deepfake prediction.
5. Return explicit "No face detected" status when applicable.
6. Create a Gradio interface with clear outputs and visual overlays.
7. Provide robust error handling and operational stability.

### 3.2 Scope Included

- Face detection and crop extraction from images and sampled video frames.
- Face-wise classification and confidence reporting.
- Aggregate summary generation.
- Visual annotation and JSON result reporting.
- Basic testing and environment setup documentation.

### 3.3 Scope Excluded

- Training a full temporal video deepfake model from raw sequence data.
- Hard real-time streaming inference optimization.
- Cloud multi-tenant deployment and role-based access control.
- Legal-grade forensic certification.

## 4. Literature and Technical Background

### 4.1 Deepfake Generation and Detection Landscape

Deepfakes are typically generated through one or more of these classes:

- Autoencoder-based face swap methods.
- GAN-based synthesis pipelines.
- Diffusion model image generation and editing.
- Neural rendering and reenactment frameworks.

Detection approaches often include:

- Spatial artifact analysis (texture inconsistencies, blending boundaries).
- Frequency-domain signatures.
- Physiological inconsistency checks.
- Vision transformer or CNN-based classification.
- Temporal inconsistency analysis in video.

This project adopts a spatial face-level classification strategy with practical engineering for deployment.

### 4.2 Why MTCNN

MTCNN is chosen for reliable face localization with confidence output and practical integration in Python. It provides:

- Multi-stage cascaded face detection.
- Good balance between speed and localization quality.
- Straightforward use for crop extraction and face scoring.

### 4.3 Why ViT Classifier

Vision Transformer models are effective for image classification tasks due to global self-attention and robust representational capacity. The selected checkpoint is specifically fine-tuned for Realism vs Deepfake classification, reducing project time while maintaining strong baseline accuracy.

## 5. System Requirements

### 5.1 Functional Requirements

- Accept image upload and return annotated image + JSON details.
- Accept video upload and return annotated preview + JSON details.
- Detect faces using MTCNN.
- Classify each detected face.
- Aggregate face-level predictions into an overall verdict.
- Handle empty/invalid input and no-face media safely.

### 5.2 Non-Functional Requirements

- Usability: easy upload and click-to-detect flow.
- Reliability: predictable outputs under edge cases.
- Maintainability: modular code organization.
- Compatibility: support CPU inference fallback.
- Explainability: show per-face scores and coordinates.

## 6. Dataset and Training Detail

### 6.1 Dataset Statement

I trained the model on a dataset that includes both real and deepfake face images. The objective was binary classification between "Realism" and "Deepfake" classes.

### 6.2 Data Composition

The dataset includes diverse visual conditions:

- Variations in lighting and color tone.
- Different face orientations and expressions.
- Multiple image qualities and compression levels.
- Mixed background complexity.

### 6.3 Preprocessing Considerations

Typical preprocessing for ViT-based image classification included:

- RGB normalization and conversion.
- Standardized resizing to model input dimensions.
- Optional augmentation during training to improve robustness.

### 6.4 Training Pipeline Summary

The model training pipeline used a ViT fine-tuning process for binary labels. Training and validation were separated to reduce overfitting and preserve generalization checks.

### 6.5 Training Risks and Bias

Any deepfake dataset can contain source bias. Potential biases include:

- Overrepresentation of particular demographic groups.
- Overfitting to synthetic artifacts from specific generators.
- Reduced robustness on unseen manipulations.

These concerns motivate threshold calibration and cautious interpretation of outputs.

## 7. Proposed Architecture

### 7.1 High-Level Architecture

The system consists of the following modules:

1. Input Layer (Gradio UI)
2. Preprocessing Layer
3. Face Detection Layer (MTCNN)
4. Classification Layer (ViT model)
5. Aggregation Layer
6. Rendering Layer (bounding boxes + labels)
7. Result Serialization Layer (JSON summary)

### 7.2 Data Flow Summary

Media input -> Face detection -> Face crop classification -> Aggregation -> Annotated output + JSON response.

### 7.3 Design Principles

- Modularity: separate files for each pipeline concern.
- Clarity: explicit data structures for face results.
- Defensive logic: no-face and invalid-input branches.
- Extensibility: easy replacement of model/detector components.

## 8. Module-Wise Design

### 8.1 Configuration Module

The configuration module centralizes constants such as:

- Face confidence threshold
- Fake score threshold
- Video frame sampling rate
- Max frame budget

Centralization improves maintainability and consistent behavior.

### 8.2 Model Service Module

Responsibilities:

- Lazy-load model and processor.
- Select CPU/GPU runtime device.
- Execute inference and softmax scoring.
- Return structured prediction object with class probabilities.

### 8.3 Face Service Module

Responsibilities:

- Lazy-load MTCNN.
- Detect faces with confidence values.
- Clip bounding boxes to valid image bounds.
- Return sorted top face detections.

### 8.4 Image Pipeline Module

Responsibilities:

- Run detection on single image.
- Handle no-face shortcut.
- Classify each face crop.
- Draw overlays and return summary.

### 8.5 Video Pipeline Module

Responsibilities:

- Decode video frames with OpenCV.
- Process every Nth frame.
- Detect and classify faces frame-wise.
- Build annotated preview clip.
- Aggregate and serialize results.

### 8.6 Aggregation Module

Responsibilities:

- Compute overall label from face-level probabilities.
- Calculate total faces, fake count, max and average scores.
- Produce no-face report consistently.

### 8.7 UI Module

Responsibilities:

- Offer separate image/video detection tabs.
- Display annotated output media.
- Display JSON details for transparent reporting.
- Provide label-orientation flip toggle.

## 9. Implementation Details

### 9.1 Language and Libraries

The implementation is in Python and uses:

- PyTorch for model execution
- Transformers for ViT model utilities
- facenet-pytorch for MTCNN
- OpenCV for video operations
- Pillow for image transforms
- Gradio for web interface

### 9.2 Code Organization

Project structure:

- `app.py`: UI and request handlers
- `src/config.py`: runtime constants
- `src/model_service.py`: classifier service
- `src/face_service.py`: face detection service
- `src/image_pipeline.py`: image workflow
- `src/video_pipeline.py`: video workflow
- `src/rendering.py`: draw overlays
- `src/aggregation.py`: summary logic
- `tests/`: basic validation tests

### 9.3 Inference Strategy

Each face crop is evaluated independently. The overall media verdict is derived from the distribution of deepfake probabilities across all evaluated faces.

## 10. Image Detection Workflow

### 10.1 Step-by-Step

1. Receive uploaded image.
2. Convert to RGB.
3. Detect faces with MTCNN.
4. If zero faces, return no-face summary.
5. For each face, run classifier.
6. Build face-level records.
7. Render boxes and labels.
8. Aggregate metrics.
9. Return annotated image + JSON.

### 10.2 Face-Level Output Fields

- Bounding box coordinates
- Face detection confidence
- Predicted class label
- Label confidence
- Deepfake probability
- Realism probability

## 11. Video Detection Workflow

### 11.1 Frame Sampling

To manage latency, the video pipeline processes every Nth frame. This allows practical throughput while preserving broad temporal coverage.

### 11.2 Frame Processing Steps

1. Open video stream.
2. Iterate through frames.
3. Skip frames based on sampling rate.
4. Detect and classify faces on sampled frames.
5. Append annotated preview frame.
6. Stop if max frame budget reached.

### 11.3 Video Summary Fields

- Sampled frame count
- Frames with faces
- Face-frame ratio
- Total faces analyzed
- Fake face count
- Max deepfake probability
- Overall verdict

## 12. Aggregation Strategy and Decision Logic

### 12.1 Rationale

A single face-level decision can be noisy. Aggregation helps stabilize final output by using all available face observations.

### 12.2 Metrics

- Maximum deepfake probability
- Average deepfake probability
- Proportion of faces above threshold

### 12.3 Final Label Rule

If the chosen aggregate signal exceeds threshold, final label is Deepfake; otherwise Realism.

### 12.4 No-Face Rule

When face list is empty, output status becomes `no_face_detected` with message `No face detected`.

## 13. User Interface Design and Experience

### 13.1 Design Goals

- Minimal actions required for inference.
- Readable output for technical and non-technical users.
- Visual proof via bounding boxes.

### 13.2 Screen Layout

- Warning banner at top.
- Two tabs: Image Detection and Video Detection.
- Detect button and output panel per tab.
- JSON details panel for transparent result inspection.

### 13.3 Label Flip Option

During runtime validation, class orientation mismatch may occur in practical deployments. A UI-level "Flip Real/Fake labels" toggle is provided to quickly align interpretation with sample behavior.

## 14. Error Handling and Reliability Strategy

### 14.1 Input Validation

- Missing media input returns informative error.
- Unreadable video raises controlled exception message.

### 14.2 Dependency Robustness

The system uses lazy imports for heavy dependencies so module import does not crash entire application during partial environment issues.

### 14.3 No-Face Robustness

No-face is treated as a first-class output state, not a hidden failure.

### 14.4 Operational Safety

Errors are returned as structured JSON messages to avoid silent failures.

## 15. Environment and Dependency Engineering

### 15.1 Python Environment

The project is validated on Python 3.11 virtual environment.

### 15.2 Compatibility Management

A key compatibility issue observed in practice: newer Transformers versions can enforce minimum Torch versions. This was resolved by pinning a stable compatible stack.

### 15.3 Pinned Runtime Example

- torch 2.2.2
- torchvision 0.17.2
- transformers 4.49.0
- facenet-pytorch 2.6.0

### 15.4 Reproducibility Consideration

Pinned requirements significantly improve reproducibility across developer systems.

## 16. Testing and Validation

### 16.1 Unit-Oriented Checks

Implemented tests validate:

- No-face aggregation behavior
- Summary output consistency
- Pipeline smoke behavior

### 16.2 Runtime Checks

- App import validation
- Dependency import validation
- Basic UI startup verification

### 16.3 Manual Functional Cases

- Face image expected labeled output
- Non-face image expected no-face output
- Face video expected frame-level analysis
- Non-face video expected no-face output

## 17. Experimental Observations

### 17.1 Qualitative Observations

- Face quality strongly affects confidence stability.
- Multiple faces in a frame provide richer aggregate evidence.
- Heavy compression can reduce confidence margins.

### 17.2 Practical Findings

- Sampling every 8th frame gives practical speed/coverage tradeoff for many clips.
- A max-frame budget prevents unbounded processing cost.

### 17.3 Label Orientation Observation

In practical usage, some samples appear semantically inverted relative to user expectation. The project includes a controlled label flip option to mitigate deployment-side interpretation mismatch.

## 18. Performance Discussion

### 18.1 Throughput Factors

Latency is influenced by:

- Number of detected faces
- Video duration and frame rate
- Sampling interval
- CPU vs GPU runtime

### 18.2 Optimization Opportunities

- Batch inference for face crops per frame.
- Optional downscaling before detection.
- Parallel decode and inference pipelines.

### 18.3 Trade-Offs

Higher frame coverage improves sensitivity but increases runtime cost. The current design prioritizes practical responsiveness.

## 19. Security, Ethics, and Responsible Use

### 19.1 Responsible Use Statement

This tool is designed for risk screening and educational or assistive analysis. It is not a legal or forensic authority.

### 19.2 Misuse Risks

- False accusations based on uncertain predictions.
- Overconfidence in single-model output.
- Privacy risks from uploading sensitive media.

### 19.3 Mitigation Measures

- Warning banner in UI.
- Confidence transparency.
- Explicit messaging on limitations.

## 20. Limitations

1. Image-trained classifier used for frame-wise video approximation.
2. Possible domain shift on unseen deepfake generation styles.
3. Sensitivity to low resolution, blur, occlusion, and heavy compression.
4. No temporal-consistency deep model in current version.
5. Potential demographic and source bias inherited from dataset.

## 21. Future Work

1. Introduce temporal transformer for sequence-level video analysis.
2. Add calibration and uncertainty estimation.
3. Build benchmark suite with balanced demographic distribution.
4. Add explainability visualizations (attention/heatmaps).
5. Implement API service mode with authentication and logging.
6. Add active-learning loop for difficult samples.

## 22. Conclusion

This project demonstrates a complete and practical deepfake detection workflow integrating face detection, transformer classification, media annotation, structured result generation, and robust edge-case handling. The system supports both image and video inputs, returns explicit no-face outputs, and provides user-facing explainability through per-face details and confidence metrics.

I trained the model workflow on a dataset of real and deepfake face images and translated that model-level capability into a deployable product with modular architecture and operational safeguards. While not a substitute for full forensic verification, the system is a strong baseline for real-world triage and a solid foundation for future research and production hardening.

## 23. References

1. Vaswani et al., "Attention Is All You Need," NeurIPS, 2017.
2. Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale," ICLR, 2021.
3. Zhang et al., "MTCNN: Joint Face Detection and Alignment Using Multi-task Cascaded Convolutional Networks," IEEE SPL, 2016.
4. Hugging Face Model Card: `prithivMLmods/Deep-Fake-Detector-v2-Model`.
5. PyTorch Documentation.
6. OpenCV Documentation.
7. Gradio Documentation.


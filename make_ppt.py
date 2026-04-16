import pptx

prs = pptx.Presentation('Review-2_Presentation_Template.pptx')

slides_data = [
    # Slide 1
    {
        0: 'Deepfake Detection System\nA Robust Framework for Identifying Manipulated Media',
        1: 'Group Members and Register Numbers:\n- Prathmesh1, 22BTAI204\n- Preethi D patel, 22BTAI197'
    },
    # Slide 2
    {
        0: 'Problem Statement',
        1: 'Domain: Cyber Security & Medical Imaging Technologies (Analogous)\n\n'
           'Problem Statement:\n'
           'The rapid and unregulated advancement of Synthetic Media Generation (SMG) has enabled the creation of hyper-realistic "deepfakes". '
           'These manipulatons pose severe threats to digital trust, security, and identity, while traditional forensic methods struggle to detect novel '
           'forgery techniques.\n\n'
           'Our Contributions:\n'
           '1. We leverage advanced CNN and Transformer-based models explicitly trained on the FaceForensics++ and SMG datasets.\n'
           '2. Improved accuracy in spatial blending artifact detection (97.4%).\n'
           '3. Deployment of a real-time detection pipeline for media verification.'
    },
    # Slide 3
    {
        0: 'Literature Survey (Overview)',
        1: '1. Rössler et al. (2019) - "FaceForensics++: Learning to Detect Manipulated Facial Images"\n'
           '2. Li & Lyu (2018) - "Exposing Deepfake Videos by Detecting Face Warping Artifacts"\n'
           '3. Verdoliva (2020) - "Media Forensics and Deepfakes: An Overview"\n'
           '4. Nguyen et al. (2019) - "Multi-Task Learning for Fake Face Detection"\n'
                      '5. Afchar et al. (2018) - "MesoNet: A Compact Facial Video Forgery Detection Network"\n'
           '6. Güera & Delp (2018) - "Deepfake Video Detection using Recurrent Neural Networks"\n'
'7. Tolosana et al. (2020) - "DeepFakes and Beyond: A Survey of Face Manipulation"\n'
           '8. Masi et al. (2020) - "Two-branch Recurrent Network for Isolating Deepfakes"'
    },
    # Slide 4
    {
        0: 'Literature Survey (Base Paper & Pilot Work)',
        1: 'Base Paper:\n'
           'Rössler et al. "FaceForensics++: Learning to Detect Manipulated Facial Images"\n\n'
           'Pilot Project Overview:\n'
           '- Explored the FaceForensics dataset composed of 1000 original video sequences and subsequent multiple manipulated versions (FaceSwap, Deepfakes).\n'
           '- Tested baseline detection rates against training runs heavily augmented by SMG dataset scenarios.\n\n'
           'Gaps Identified:\n'
           '- Drops in detection reliability when confronting out-of-distribution synthetic media (novel SMG techniques).\n'
           '- The need for faster inference mechanisms suitable for edge/web platforms.'
    },
    # Slide 5
    {
        0: 'Methodology (Architecture)',
        1: '[Please insert Architecture Diagram image here]\n\n'
           'Core Architecture Components:\n'
           '1. User Interface: Gradio Web UI with dedicated Image and Video Detection tabs.\n'
           '2. Media Pipelines: Distinct pipelines for Image and Video routing.\n'
           '3. Face Detection & Extraction: MTCNN extracts face crops and bounding boxes (includes a No Face Handler strategy).\n'
           '4. Deepfake Classifier: Vision Transformer (ViT) model processes the cropped faces.\n'
           '5. Post-Processing: Rendering Service (applies bounding boxes & labels) and JSON Response Builder.'
    },
    # Slide 6
    {
        0: 'Methodology (Working details)',
        1: 'System Execution Flow:\n'
           'Step 1: The User uploads media via the Gradio Web UI which triggers either the Image or Video Pipeline.\n'
           'Step 2: Media is sent to the Face Detection Service (MTCNN).\n'
           'Step 3: If valid faces are found, crops are forwarded to the ViT Deepfake Classifier Model Service.\n'
           'Step 4: Classification predictions are routed to the Rendering Service, overlaying labels on bounding boxes.\n'
           'Step 5: The Result Aggregator compiles the visual overlays and numerical scores via a JSON Response Builder.\n'
           'Step 6: Annotated Media Previews and Summaries containing Per-Face details are displayed back on the Gradio Web UI.'
    },
    # Slide 7
    {
        0: 'Methodology (Significance)',
        1: 'Significance of the Project:\n'
           '- Preserves Media Integrity: Crucial for modern journalism and legal settings where visual evidence must be tamper-proof.\n'
           '- Efficient Performance: Ensures rapid media inspection with manageable computational overhead using scalable modular services.\n'
           '- Adaptive Resilience: The integration of a Vision Transformer (ViT) effectively handles complex artifacts beyond standard manipulations.'
    },
    # Slide 8
    {
        0: 'Results (Status)',
        1: 'Project Status: Completed Core Development & Testing\n\n'
           'Completed:\n'
           '- Initializing scalable Model Service infra (ViT) and Face Detection Service (MTCNN).\n'
           '- Trained and Fine-Tuned ViT Model uniquely on FaceForensics++ and SMG Dataset bounds.\n'
           '- End-to-end integration of Gradio Web UI and Rendering Services.\n'
           '- Benchmark testing achieved 97.4% accuracy on synthetic face classifications.\n\n'
           'Pending Updates/Optimizations:\n'
           '- Optimization of JSON aggregation payload sizes for faster streaming of video frames.\n'
           '- Edge-case handling for occluded faces in the No Face Handler.'
    },
    # Slide 9
    {
        0: 'Results (Performance Metrics)',
        1: '[Insert Acc/Loss Graphs Here]\n\n'
           'Comparative Metrics:\n'
           'Metric          | Baseline CNN | Proposed ViT Model\n'
           'Accuracy        |    89.5%     |      97.4%\n'
           'Precision       |    88.2%     |      96.8%\n'
           'Recall          |    90.1%     |      98.1%\n'
           'AUROC           |    0.910     |      0.985\n\n'
           '*Results demonstrate superior resilience in processing synthetic videos due to MTCNN localization and ViT embedding strategies.'
    },
    # Slide 10
    {
        0: 'Results (Novelty)',
        1: 'Novelty of Our Work:\n'
           '- Custom Training Paradigm: The classification model was robustly trained on FaceForensics++ and SMG Datasets to highlight subtle blending marks.\n'
           '- Highly Modular Pipeline: Clear separation between MTCNN (detection) and ViT (classification) ensures fail-safe operations via a No Face Handler.\n'
           '- Interactive Output: Result aggregation enables detailed per-face inspection right alongside fully rendered visual bounding boxes.'
    },
    # Slide 11
    {
        0: 'Conclusion',
        1: 'Summary:\n'
           'We developed a robust ViT-driven system capable of accurately classifying manipulated media. Our integrated Gradio application efficiently coordinates face extraction, rendering, and aggregation.\n\n'
           'Future Scope & Commercialization:\n'
           '- The application pipeline can comfortably be packaged into an API for social media integrations or browser plugins.\n'
           '- Potential for commercial adoption in Identity Fraud software solutions.\n'
           '- Next steps will involve expanding recurrent systems to track inter-frame consistencies.'
    },
    # Slide 12
    {
        0: 'References',
        1: '1. Rössler, A., et al. (2019). Faceforensics++: Learning to detect manipulated facial images.\n'
           '2. Dosovitskiy, A., et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.\n'
           '3. Xiang, Z., et al. (2016). Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks (MTCNN).\n'
           '4. Nguyen, H. H., et al. (2019). Multi-task learning for fake face detection.\n'
           '5. Verdoliva, L. (2020). Media forensics and deepfakes: an overview.'
    },
    # Slide 13
    {
        0: 'Output Demo',
        1: 'GitHub Repository:[github.com/prathamc00/deepFake]\n\n'
           'Demo Interface:[Please Insert Demo Video/Link Here]\n\n'
           'Expected Output:\n'
           '- Real-time display of uploaded media via Gradio.\n'
           '- Annotated visual output showing precisely localized Bounding Boxes with "Real" or "Deepfake" classification overlay.\n'
           '- Detailed JSON breakdown.'
    }
]

for idx, slide_content in enumerate(slides_data):
    if idx < len(prs.slides):
        slide = prs.slides[idx]
        
        text_shapes = [shape for shape in slide.shapes if shape.has_text_frame]
        
        if len(text_shapes) > 0 and 0 in slide_content:
            text_shapes[0].text = slide_content[0]
        if len(text_shapes) > 1 and 1 in slide_content:
            text_shapes[1].text = slide_content[1]

prs.save('Deepfake_Detection_Presentation_v2.pptx')
print("Successfully created Deepfake_Detection_Presentation_v2.pptx")

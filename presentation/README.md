# Presentation Deliverables

This directory contains the presentation slides and automation scripts for **IntelliArchive: Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models** (Course: **BCSE355L – Cloud Architecture Design**).

---

## 📂 Deliverables

1. **`IntelliArchive_Final_Presentation.pptx`**  
   - Comprehensive 16:9 widescreen presentation deck (13 slides).
   - Designed using a custom aerospace dark-navy palette matching the web platform.
   - Includes full system architecture, Vision Foundation Model pipeline, SpaceNet evaluation charts, AWS cost models, ECR container verification, test suite audit, and team contribution breakdown.

2. **`build_presentation.py`**  
   - Python script utilizing `python-pptx` to programmatically generate or regenerate the presentation deck with high-resolution chart assets from `results/`.

---

## 🖥️ Slide Deck Outline

| Slide # | Title | Content Focus |
|---|---|---|
| **1** | Title Slide | Course code, project title, student registration numbers, faculty guide. |
| **2** | Problem Statement | Failures of static, time-based S3 lifecycle rules; content-blind limitations. |
| **3** | Objectives & Novelty | Zero-shot semantic scoring, dynamic tiering, automated cost optimization. |
| **4** | Architecture Comparison | Implemented Local Prototype vs. Proposed AWS Production Cloud. |
| **5** | Vision Model Pipeline | Radiometric GeoTIFF preprocessing, CLIP ViT-B/32 zero-shot prompt anchors, composite formula. |
| **6** | Dual Storage Engine | Atomic local directory tiering + live private AWS S3 bucket integration (`ap-south-1`). |
| **7** | SpaceNet Results | Evaluation on Las Vegas dataset; importance score distributions. |
| **8** | Cloud Cost Model | Flat S3 Standard vs. Tiered storage model; ~49% monthly cost reduction. |
| **9** | Containerization & ECR | Docker CPU wheel optimization (1.36 GB) pushed to Amazon ECR. |
| **10** | Automated Test Audit | 41/41 passing pytest tests across storage, S3 service, and web endpoints. |
| **11** | Work Distribution | Detailed individual contributions (24BIT0580 & 24BIT0129). |
| **12** | Conclusion & Roadmap | Key takeaways, Amazon Bedrock & DynamoDB production roadmap. |
| **13** | Q&A / Closing | Acknowledgments and technical discussion. |

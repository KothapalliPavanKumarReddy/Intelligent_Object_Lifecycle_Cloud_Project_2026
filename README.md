# Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models

## 📖 Project Overview

This project is developed as part of the **BCSE355L – Cloud Architecture Design** course.

The project presents a content-aware cloud storage lifecycle management approach for satellite image archives. Instead of relying only on file age, the prototype uses a Vision Foundation Model (CLIP) to estimate the semantic relevance of satellite images and map the resulting importance categories to different storage tiers.

The current implementation uses a **local S3 storage simulation** to demonstrate the lifecycle decisions without requiring live AWS resources.

---

## 👨‍💻 Team Members

| Registration Number | Name |
|---------------------|------|
| 24BIT0580 | K. Pavan Kumar Reddy |
| 24BIT0129 | Anhad |

---

## 🎯 Problem Statement

Traditional cloud storage lifecycle policies primarily rely on object age or predefined transition rules.

For large satellite image archives, a content-aware approach can provide an additional decision signal by considering the semantic relevance of individual images.

This project explores a prototype framework that analyzes satellite images using a Vision Foundation Model and assigns them to different storage tiers according to their semantic importance.

---

## 🎯 Objectives

- Develop a content-aware lifecycle management prototype for satellite image archives.
- Apply a Vision Foundation Model for semantic image analysis.
- Generate semantic importance scores for satellite images.
- Classify images into LOW, MEDIUM, and HIGH importance categories.
- Map importance categories to simulated cloud storage tiers.
- Record lifecycle decisions for analysis and auditing.
- Visualize importance scores and storage-tier distributions.
- Design a proposed AWS architecture for future cloud deployment.

---

## 🏗️ System Architecture

The project consists of the following processing stages:

```text
Satellite Images
       |
       v
Image Preprocessing
       |
       v
CLIP Vision Foundation Model
       |
       v
Semantic Importance Score
       |
       v
Importance Classification
       |
       +-----------------------------+
       |             |               |
       v             v               v
     LOW          MEDIUM            HIGH
       |             |               |
       v             v               v
S3_GLACIER   S3_STANDARD_IA     S3_STANDARD
       |             |               |
       +-------------+---------------+
                     |
                     v
            Lifecycle Decision Log
                     |
                     v
              Results Dashboard
```

---

## 🧠 AI Model

The prototype uses:

**OpenAI CLIP — `openai/clip-vit-base-patch32`**

The model compares each satellite image with text prompts representing different levels of semantic importance.

The resulting probabilities are converted into a prototype semantic importance score.

### Important limitation

The generated importance score is a prototype semantic relevance measure. It has not been scientifically validated as an objective measure of the archival value or future usefulness of a satellite image.

---

## ☁️ Storage Lifecycle Strategy

The prototype maps importance categories to simulated S3 storage tiers:

| Importance Category | Simulated Storage Tier |
|---------------------|------------------------|
| LOW | S3_GLACIER |
| MEDIUM | S3_STANDARD_IA |
| HIGH | S3_STANDARD |
🛠️ Technology Stack
| Category                | Technology            |
| ----------------------- | --------------------- |
| Programming             | Python 3.11           |
| AI Model                | OpenAI CLIP           |
| Image Processing        | Pillow                |
| Data Processing         | Pandas                |
| Visualization           | Matplotlib            |
| Cloud Concept           | Amazon S3             |
| Cloud Lifecycle Concept | S3 Lifecycle Policies |
| Proposed Compute        | AWS Lambda            |
| Proposed ML Deployment  | Amazon SageMaker      |
| Proposed Monitoring     | Amazon CloudWatch     |
| Proposed Notifications  | Amazon SNS            |
| Proposed Access Control | AWS IAM               |
| Version Control         | Git & GitHub          |
📂 Dataset

Dataset: SpaceNet satellite imagery sample

The prototype uses a small sample of 10 satellite images for experimentation and demonstration.

The downloaded raw and processed image datasets are intentionally excluded from Git tracking where appropriate because of dataset size.

The project therefore stores the processing code and generated results in the repository while the local dataset remains available in the development environment.
📁 Repository Structure
Intelligent_Object_Lifecycle_Cloud_Project_2026/
│
├── architecture/
│   └── architecture.md
│
├── cloud_simulation/
│   ├── S3_STANDARD/
│   ├── S3_STANDARD_IA/
│   └── S3_GLACIER/
│
├── dataset/
│   └── README.md
│
├── results/
│   ├── importance_scores.csv
│   ├── importance_scores_chart.png
│   ├── category_distribution.png
│   ├── storage_distribution.png
│   ├── lifecycle_log.csv
│   └── README.md
│
├── src/
│   ├── ai_model/
│   │   ├── preprocessing.py
│   │   └── importance_scoring.py
│   │
│   ├── cloud/
│   │   └── s3_lifecycle.py
│   │
│   └── dashboard/
│       └── dashboard.py
│
├── .gitignore
├── requirements.txt
└── README.md
🔄 Processing Pipeline
1. Image Preprocessing

Satellite TIFF images are:

loaded using Pillow
converted to RGB
resized to 224 × 224
saved as JPEG files for model processing
2. Importance Scoring

The processed images are passed through the CLIP model.

The model compares the image against importance-related text prompts and produces probabilities.

These probabilities are converted into a prototype semantic importance score.

3. Importance Classification

The prototype uses the following classification thresholds:
| Score | Category |
| ----: | -------- |
|  ≥ 70 | HIGH     |
|  ≥ 40 | MEDIUM   |
|  < 40 | LOW      |
4. Storage Mapping

The category is mapped to a simulated storage tier.

5. Lifecycle Simulation

The lifecycle module copies the processed image into the corresponding local storage-tier directory and records the decision.

6. Dashboard

The dashboard generates visualizations for:

individual image importance scores
importance category distribution
simulated storage-tier distribution
📊 Prototype Results

The prototype was tested on 10 processed satellite images.

Importance Category Distribution
| Category  | Number of Images |
| --------- | ---------------: |
| LOW       |                6 |
| MEDIUM    |                4 |
| HIGH      |                0 |
| **Total** |           **10** |
Simulated Storage-Tier Distribution
| Storage Tier   | Number of Images |
| -------------- | ---------------: |
| S3_GLACIER     |                6 |
| S3_STANDARD_IA |                4 |
| S3_STANDARD    |                0 |
| **Total**      |           **10** |
The current 10-image sample produced no HIGH-category images under the prototype scoring thresholds. This result is reported as observed rather than artificially adjusted.

## 📈 Generated Results

The project generates the following result files:

- `results/importance_scores.csv` — semantic importance scores and storage classifications
- `results/lifecycle_log.csv` — lifecycle decisions
- `results/importance_scores_chart.png` — importance score visualization
- `results/category_distribution.png` — importance category distribution
- `results/storage_distribution.png` — simulated storage-tier distribution

---

## ☁️ Current Cloud Deployment Status

The current project is a **local prototype**.

The storage lifecycle is simulated using local folders rather than live AWS S3 resources.

### Implemented

- Image preprocessing
- CLIP-based semantic scoring
- Importance classification
- Storage-tier mapping
- Local S3 lifecycle simulation
- Lifecycle decision logging
- Results visualization
- Proposed cloud architecture

### Proposed Future AWS Deployment

The proposed production architecture can use:

- Amazon S3
- AWS Lambda
- Amazon SageMaker
- Amazon CloudWatch
- Amazon SNS
- AWS IAM
- S3 Lifecycle Policies

The proposed AWS architecture is documented in:

`architecture/architecture.md`

---

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Intelligent_Object_Lifecycle_Cloud_Project_2026

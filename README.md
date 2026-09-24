# Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models

## 📖 Project Overview

This project is developed as part of the **BCSE355L – Cloud Architecture Design** course.

The project proposes an intelligent cloud-based lifecycle management system for satellite image archives using Vision Foundation Models. Instead of using traditional time-based lifecycle policies, the system analyzes the semantic importance of satellite images and automatically assigns them to appropriate AWS S3 storage tiers, thereby reducing storage costs while preserving access to high-value imagery.

---

## 👨‍💻 Team Members

| Registration Number | Name |
|---------------------|---------------------------|
| 24BIT0580 | K. Pavan Kumar Reddy |
| 24BIT0129 | Anhad |

---

## 🎯 Problem Statement

Traditional cloud storage lifecycle policies rely mainly on the age of files for storage tier transitions. This approach is inefficient for satellite image archives because important images may be archived too early while less useful images continue occupying expensive storage.

This project introduces an intelligent content-aware lifecycle management framework using Vision Foundation Models to classify image importance and automate storage tier optimization.

---

## 🎯 Objectives

- Develop a content-aware lifecycle management system for satellite image archives.
- Integrate Vision Foundation Models for semantic image analysis.
- Reduce cloud storage cost using AWS S3 storage tiers.
- Automate lifecycle transitions using AWS services.
- Improve retrieval efficiency for important satellite images.

---

## ☁️ Proposed AWS Architecture

The proposed architecture consists of:

- Amazon S3
- AWS Lambda
- Amazon SageMaker
- Amazon CloudWatch
- Amazon SNS
- AWS IAM

The complete architecture diagrams are available inside the **architecture/** folder.

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Cloud Platform | AWS |
| Storage | Amazon S3 |
| Compute | AWS Lambda |
| AI | Vision Foundation Models (CLIP / DINOv2) |
| Database | DynamoDB (Planned) |
| Dashboard | Streamlit |
| Version Control | Git & GitHub |

---

## 📂 Dataset

**Dataset Name:** SpaceNet Dataset

Purpose:
- Satellite image classification
- Lifecycle optimization
- Cloud storage evaluation

Dataset details are available inside the **dataset/** folder.

---

## 📁 Repository Structure
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
│   ├── raw/
│   ├── sample/
│   └── processed/
│
├── results/
│   ├── importance_scores.csv
│   ├── importance_scores_chart.png
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
└── README.md

## 📌 Current Project Status

### Completed

✅ Literature Survey Completed

✅ Research Gap Analysis Completed

✅ AWS Architecture Planning Completed

✅ Dataset Selection Completed

✅ Repository Structure Completed

✅ Satellite Image Preprocessing Completed

✅ CLIP Vision Foundation Model Integrated

✅ Semantic Importance Scoring Implemented

✅ Importance-Based Storage Classification Implemented

✅ Local S3 Lifecycle Simulation Implemented

✅ Lifecycle Decision Logging Implemented

✅ Results Visualization Implemented

### Prototype Results

The prototype was tested on 10 processed satellite images.

| Category | Number of Images |
|----------|-----------------:|
| LOW | 6 |
| MEDIUM | 4 |
| HIGH | 0 |

### Storage-Tier Distribution

| Simulated Storage Tier | Number of Images |
|------------------------|-----------------:|
| S3_GLACIER | 6 |
| S3_STANDARD_IA | 4 |
| S3_STANDARD | 0 |

### Generated Results

- `results/importance_scores.csv` — semantic importance scores
- `results/lifecycle_log.csv` — lifecycle decisions
- `results/importance_scores_chart.png` — importance-score visualization

### Cloud Deployment Status

The current implementation uses local folders to simulate AWS S3 storage tiers.

Real AWS deployment is planned as a future stage.

The proposed AWS architecture includes Amazon S3, AWS Lambda, Amazon SageMaker, Amazon CloudWatch, Amazon SNS, and AWS IAM.

## 📚 Course Information

**Course:** BCSE355L – Cloud Architecture Design

**Project Phase:** Phase-I

---

---

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Intelligent_Object_Lifecycle_Cloud_Project_2026

## 📄 License

This repository is created for academic purposes as part of the Cloud Architecture Design course.

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
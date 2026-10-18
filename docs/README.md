# Project Documentation

This directory contains the academic reports and technical documentation for **IntelliArchive: Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models** (Course: **BCSE355L – Cloud Architecture Design**, VIT Vellore).

---

## 📂 Documentation Deliverables

| File | Format | Description |
|---|---|---|
| **`Final_Project_Report.docx`** | Microsoft Word (.docx) | Publication-grade comprehensive final technical report formatted for academic submission, including cover page, tables, figures, formulas, and individual contribution tables. |
| **`Final_Project_Report.md`** | Markdown (.md) | Complete final technical report in GitHub Flavored Markdown with KaTeX formulas, architecture diagrams, and cost breakdown tables. |
| **`Cloud_Architecture_Project_Phase1_Report (2).docx`** | Microsoft Word (.docx) | Initial Phase-I project proposal report submitted during project review. |
| **`build_report_docx.py`** | Python Script | Automated script using `python-docx` to compile and format `Final_Project_Report.docx` directly from project data and result charts. |

---

## 📑 Report Structure & Contents

1. **Executive Summary & Abstract**
2. **Problem Statement & Motivation:** Limitations of chronological and prefix-based S3 lifecycle rules.
3. **System Architecture & Dual Execution Model:** Side-by-side comparison of the implemented local prototype vs. proposed AWS cloud production architecture (ECS Fargate + S3 + DynamoDB + Bedrock).
4. **Vision Foundation Model Methodology:** 16-bit GeoTIFF dynamic contrast stretching, OpenAI CLIP ViT-B/32 zero-shot semantic prompt pairs, and composite scoring formula.
5. **Experimental Results & Cost Optimization:** Evaluation on SpaceNet Las Vegas satellite imagery; empirical comparison of Flat S3 Standard vs. Content-Aware Tiering (~49% cost savings).
6. **Containerization & Amazon ECR Verification:** Docker CPU-only PyTorch wheel optimization (1.36 GB) registered in Amazon ECR (`ap-south-1`).
7. **Automated Test Suite Verification:** Audit of the 41 passing automated tests in `tests/`.
8. **Work Distribution & Team Contributions:** Granular matrix of individual student contributions (24BIT0580 & 24BIT0129).
9. **Conclusion & Future Roadmap**

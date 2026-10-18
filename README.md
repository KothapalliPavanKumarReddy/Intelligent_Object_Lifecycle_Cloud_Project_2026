# Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models (IntelliArchive)

## 📖 Project Overview

This project is developed as part of the **BCSE355L – Cloud Architecture Design** course.

Traditional cloud storage lifecycle policies (such as AWS S3 Lifecycle configurations) rely almost exclusively on object age, prefix matching, or fixed transition schedules. In massive satellite imagery repositories, age alone does not reflect operational value: high-resolution imagery containing critical urban infrastructure or active disaster zones often retains high utility indefinitely, whereas cloud-covered or low-detail imagery can be safely archived immediately.

**IntelliArchive** demonstrates a content-aware storage lifecycle management prototype. It combines a local Vision Foundation Model (**OpenAI CLIP ViT-B/32**) for semantic evaluation with an asynchronous **FastAPI** web platform, local cloud tiering simulation, and real **Amazon S3** integration.

---

## 👨‍💻 Team Members

| Registration Number | Name |
|---|---|
| **24BIT0580** | K. Pavan Kumar Reddy |
| **24BIT0129** | Anhad |

---

## 🎯 Objectives

- **Content-Aware Lifecycle Management:** Evaluate satellite imagery semantics alongside traditional metadata to make informed storage decisions.
- **Vision Foundation Model Inference:** Use zero-shot classification via OpenAI CLIP (`openai/clip-vit-base-patch32`) to generate semantic importance scores.
- **Lifecycle Classification & Tiering:** Classify images into `HIGH`, `MEDIUM`, and `LOW` categories and map them to corresponding storage classes (`S3_STANDARD`, `S3_STANDARD_IA`, `S3_GLACIER`).
- **Local Cloud Simulation & Ledger:** Simulate S3 storage buckets locally (`cloud_simulation/`) while maintaining audit trails in `results/lifecycle_log.csv` and `results/importance_scores.csv`.
- **Real AWS S3 Integration:** Provide direct integration with a private AWS S3 bucket for listing and uploading processed satellite objects.
- **Interactive Web Interface:** Provide a comprehensive FastAPI web application for inference, archive exploration, cost analysis, and system architecture visualization.
- **Containerization & Cloud Design:** Package the application via Docker and design a scalable, serverless AWS deployment architecture (ECS Fargate, S3, DynamoDB, Bedrock).

---

## 🌐 FastAPI Web Application Features

The web interface is built using FastAPI, Jinja2 server-side rendering, and Chart.js, themed with a custom aerospace dark-mode design system. It consists of five primary views:

1. **Executive Dashboard (`/`):**
   - Live KPI summary cards: Total Images, Category Distributions (`HIGH`, `MEDIUM`, `LOW`), Storage Class breakdown, and Average Importance Score.
   - Interactive Chart.js graphs displaying storage tier allocation and importance score spreads.
   - Real-time recent activity ledger tracking the last 15 lifecycle decisions.
2. **Interactive Analysis & Inference (`/analyze`):**
   - Supports uploading user satellite imagery (`.tif`, `.tiff`, `.png`, `.jpg`, `.jpeg` up to 50 MB) or selecting bundled SpaceNet sample GeoTIFFs.
   - On-the-fly 16-bit to 8-bit dynamic contrast stretching for web preview.
   - Real-time CLIP zero-shot inference, displaying normalized probability distributions, computed importance score, assigned category, and target storage class.
   - Option to automatically commit the result to the local simulation storage tiers and audit logs.
3. **Archive Browser (`/archive`):**
   - Filterable catalog of archived imagery with category pills (`ALL`, `HIGH`, `MEDIUM`, `LOW`) and storage class dropdowns.
   - Live search filter by filename.
   - Real **AWS S3 Storage Panel**: Lists live objects in the configured private S3 bucket (`satellite-images/` prefix) and allows direct uploading of processed imagery to AWS S3.
4. **Analytics & Cost Optimization (`/analytics`):**
   - Statistical metrics: Median, standard deviation, minimum, and maximum importance scores.
   - Importance score distribution histogram.
   - **Cloud Cost Model:** Compares flat S3 Standard storage costs against optimized tiering (S3 Standard @ $0.023/GB, S3 Standard-IA @ $0.0125/GB, S3 Glacier Flexible Retrieval @ $0.004/GB), highlighting projected percentage and monthly cost savings.
5. **System Architecture (`/architecture`):**
   - Side-by-side technical comparison of the **Current Local Prototype** vs. the **Proposed AWS Cloud Production Architecture**.
   - Interactive tier mapping and workflow explanations for academic demonstration.

---

## 🧠 CLIP Vision Foundation Model Scoring

### Preprocessing
Satellite GeoTIFF imagery typically contains 16-bit radiometric values clustered near zero. Before inference:
1. `enhance_satellite_image()` applies dynamic min-max percentile contrast stretching across color channels to map values to `[0, 255]`.
2. The image is resized to `224 × 224` pixels RGB, matching the input resolution expected by the CLIP vision transformer.

### Zero-Shot Importance Inference
The system uses the `openai/clip-vit-base-patch32` foundation model. Text prompt embeddings represent three semantic relevance levels:
- **High Importance:** `"important satellite image containing urban infrastructure"`
- **Medium Importance:** `"moderately important satellite image"`
- **Low Importance:** `"unimportant satellite image with little useful information"`

Softmax probabilities $P(\text{High})$, $P(\text{Medium})$, and $P(\text{Low})$ are extracted, and a composite score is computed:

$$\text{Score} = (P(\text{High}) \times 100) + (P(\text{Medium}) \times 50) + (P(\text{Low}) \times 0)$$

### Tier Assignment Thresholds
- **HIGH** ($\ge 70.0$) $\rightarrow$ `S3_STANDARD` (frequent access, mission-critical infrastructure)
- **MEDIUM** ($\ge 40.0$, $< 70.0$) $\rightarrow$ `S3_STANDARD_IA` (infrequent access, moderate detail)
- **LOW** ($< 40.0$) $\rightarrow$ `S3_GLACIER` (cold archival, minimal structural information)

> [!NOTE]
> **Prototype Disclaimer:** This semantic scoring mechanism is an academic proof-of-concept designed to demonstrate content-aware lifecycle tiering. The zero-shot prompt weighting is a heuristic prototype and is **not** an operationally validated measure of geospatial, scientific, or archival significance.

---

## 💻 Local Setup & Execution

### Prerequisites
- Python 3.10 or 3.11 (tested on Python 3.11.9)
- Git and PowerShell / Bash

### Installation

1. Open PowerShell in the project directory:
   ```powershell
   cd C:\Users\Pavan\Intelligent_Object_Lifecycle_Cloud_Project_2026
   ```

2. Activate the existing virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Ensure dependencies from `requirements.txt` are installed:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Web Platform

Start the Uvicorn ASGI server:
```powershell
python web/app.py
```
*Alternatively:*
```powershell
uvicorn web.app:app --host 127.0.0.1 --port 8000 --reload
```

Access the application in your browser at:
```
http://127.0.0.1:8000
```

---

## 🧪 Automated Testing

The repository contains automated unit and integration tests covering storage management, AWS S3 service integration, and web endpoints.

Run the test suite using pytest:
```powershell
.\.venv\Scripts\pytest.exe -v
```

#### Verified Test Results
During the formal audit run, all **41 tests passed** (100% test pass rate):
```text
tests/test_lifecycle_storage.py . . . . . . . . . .                      [ 24%]
tests/test_s3_service.py . . . . . . . . . . . . . . . . . . . . . . . .  [ 82%]
tests/test_web_app.py . . . . . . .                                      [100%]
================= 41 passed, 3 warnings in 279.33s (0:04:39) ==================
```

---

## ☁️ Amazon S3 Integration & Configuration

The application includes live AWS S3 integration via `web/services/s3_service.py` to interact with private cloud storage.

### Target S3 Bucket
- **Bucket Name:** `intelliarchive-pavan-satellite-2026`
- **Region:** `ap-south-1` (Asia Pacific - Mumbai)
- **Access:** Private S3 bucket with Block Public Access enabled.

### Environment Configuration
The service reads configuration strictly from environment variables without hardcoded credentials:

| Variable | Description | Default / Example |
|---|---|---|
| `INTELLIARCHIVE_S3_BUCKET` | Target AWS S3 bucket name | `intelliarchive-pavan-satellite-2026` |
| `AWS_REGION` | AWS region hosting the bucket | `ap-south-1` |
| `AWS_PROFILE` | Named AWS CLI profile for local dev | `intelliarchive` (set to `""` in production) |

For local testing, configure an AWS CLI profile:
```powershell
aws configure --profile intelliarchive
```
In production (e.g., AWS ECS Fargate), `AWS_PROFILE` is left blank to automatically inherit IAM Task Role credentials.

---

## 🐳 Docker Deployment & Local Verification

The project includes a production-ready [Dockerfile](Dockerfile) and [.dockerignore](.dockerignore) designed for containerized deployment.

### Features of the Docker Image
- Base: `python:3.11-slim` with unprivileged `appuser`.
- Utilizes official CPU-only PyTorch wheels (`--index-url https://download.pytorch.org/whl/cpu`), drastically trimming the image footprint from ~12 GB down to **1.36 GB**.
- Pre-downloads and caches CLIP ViT-B/32 weights during build time (`HF_HUB_DISABLE_XET=1` with retry-safe execution) to eliminate network download latency during cold starts.
- Built-in container healthcheck querying `http://localhost:8080/`.

### Building and Running Locally

1. **Build Image:**
   ```powershell
   docker build -t intelliarchive:latest .
   ```

2. **Run Container Locally:**
   ```powershell
   docker run -d --name intelliarchive-test -p 8080:8080 intelliarchive:latest
   ```

3. **Verify Health:**
   ```powershell
   docker ps
   # Check logs
   docker logs intelliarchive-test
   # Test endpoints
   curl http://localhost:8080/
   curl http://localhost:8080/api/summary
   ```

---

## 🚀 AWS Cloud Deployment Status

| Component | Target Architecture | Current Status |
|---|---|---|
| **Amazon S3** | Private Bucket (`intelliarchive-pavan-satellite-2026`) | **Active & Verified** (Region: `ap-south-1`) |
| **Amazon ECR** | Private Repository (`intelliarchive`) | **Active & Verified** (Registry: `371234372967.dkr.ecr.ap-south-1.amazonaws.com`) |
| **Docker Image Push** | Tag and push to ECR repository | **Active & Verified** (Image Tag: `cpu-test`, 1.36 GB CPU-optimized PyTorch image pushed) |
| **AWS ECS / Fargate** | Serverless container task running web platform | **Configured & Ready** (Task Definition: `src/aws/ecs-task-definition.json`) |
| **Amazon DynamoDB** | Distributed metadata and lifecycle audit table | **Proposed Architecture** (Represented locally by atomic CSV ledgers) |

---

## 📁 Academic Deliverables

- **Presentation Slides:** [`presentation/IntelliArchive_Final_Presentation.pptx`](presentation/IntelliArchive_Final_Presentation.pptx) (16:9 widescreen presentation deck with aerospace styling and evaluation charts).
- **Final Project Technical Report:**
  - Microsoft Word Document: [`docs/Final_Project_Report.docx`](docs/Final_Project_Report.docx)
  - GitHub Markdown Document: [`docs/Final_Project_Report.md`](docs/Final_Project_Report.md)


---

## 🏛️ Local Simulation vs. Proposed Production Architecture

```text
+-----------------------------------------------------------------------------------------+
|                                    INTELLIARCHIVE                                       |
+-----------------------------------------------------------------------------------------+
| LOCAL SIMULATION PROTOTYPE (Implemented)  | PROPOSED AWS PRODUCTION ARCHITECTURE        |
+-------------------------------------------+---------------------------------------------+
| • Local FastAPI server (Uvicorn / Docker)  | • AWS ECS Fargate (Serverless Container)    |
| • PyTorch CLIP running on local CPU        | • Amazon Bedrock (Claude / Titan Multimodal)|
| • Directory tiers (cloud_simulation/*)    | • AWS S3 Intelligent-Tiering / Lifecycle    |
| • Local CSV files (importance_scores.csv) | • Amazon DynamoDB (Metadata & Audit Ledger) |
| • Direct file system uploads              | • S3 Pre-signed Uploads via API Gateway     |
| • Local development AWS CLI profiles      | • IAM Task Roles (Zero persistent keys)     |
+-------------------------------------------+---------------------------------------------+
```

---

## ⚠️ Limitations & Considerations

1. **Ephemeral Container Storage:**
   In Docker and AWS ECS Fargate, local file system modifications (such as files written to `/app/web/uploads` or `/app/cloud_simulation`) are ephemeral and reset when tasks restart. For production persistence, image storage must be mapped exclusively to Amazon S3.
2. **Docker Image Size:**
   The initial Docker image is ~12 GB due to default PyTorch packages including CUDA/NVIDIA shared libraries. A planned future optimization is switching to the CPU-only PyTorch wheel (`--index-url https://download.pytorch.org/whl/cpu`), which reduces the image size to ~3.2 GB.
3. **Model Generalization:**
   CLIP ViT-B/32 was trained on general web image-text pairs rather than dedicated remote-sensing corpora (such as RemoteCLIP or specialized earth observation models). Prompt sensitivity can influence scoring distributions across different satellite terrains.
4. **Security Notes:**
   - No credentials or access keys are committed.
   - S3 operations use least-privilege IAM policies.
   - Production deployments must rely on IAM Task Roles by keeping `AWS_PROFILE=""`.
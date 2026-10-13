# IntelliArchive — Web Platform

**AI-Powered Satellite Object Lifecycle Optimization for Satellite Image Archives**

---

## 1. Architecture Overview

IntelliArchive is a content-aware cloud storage management and analytics platform built on top of the satellite image processing research pipeline. Instead of relying solely on object age or static schedules, IntelliArchive utilizes a Vision Foundation Model (OpenAI CLIP ViT-B/32) to compute semantic importance scores for high-resolution satellite imagery (GeoTIFFs) and dynamically assigns them to optimal cloud storage tiers.

### End-to-End Workflow

```text
Satellite Images (TIFF/PNG/JPG)
      │
      ▼
Image Preprocessing (Dynamic Contrast Stretching + Resize to 224x224 RGB)
      │
      ▼
Vision Foundation Model (OpenAI CLIP ViT-B/32 Zero-Shot Inference)
      │
      ▼
Semantic Importance Scoring (Probabilistic weighting over semantic prompts)
      │
      ▼
Lifecycle Classification:
  ├── HIGH   (Score ≥ 70) ──► S3_STANDARD     (Immediate, frequent access)
  ├── MEDIUM (Score ≥ 40) ──► S3_STANDARD_IA  (Infrequent access tier)
  └── LOW    (Score < 40)  ──► S3_GLACIER      (Cold archival tier)
      │
      ▼
Storage Synchronization & Audit Logging:
  ├── Simulated Cloud Tiering: cloud_simulation/{TIER}/
  ├── Scores Ledger: results/importance_scores.csv
  └── Audit Log: results/lifecycle_log.csv
      │
      ▼
IntelliArchive Web Platform (Dashboard, Real-time Inference, Archive & Analytics)
```

---

## 2. Installation & Requirements

Ensure you are using Python 3.10+ with the project's virtual environment activated:

```bash
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt
```

Core dependencies:
- **FastAPI** (`fastapi`): High-performance asynchronous web framework
- **Uvicorn** (`uvicorn`): ASGI production server
- **Jinja2** (`jinja2`): Server-side templating engine
- **Python Multipart** (`python-multipart`): File upload parsing
- **Transformers & PyTorch** (`transformers`, `torch`): OpenAI CLIP ViT-B/32 foundation model
- **Pillow & NumPy** (`pillow`, `numpy`): Satellite contrast stretching and image array handling
- **Pandas** (`pandas`): Dynamic metadata, CSV parsing, and statistical aggregation

---

## 3. Running Locally

You can launch the web application with either of the following commands from the repository root:

### Option A: Direct Python runner (Recommended)

```bash
python web/app.py
```

### Option B: Uvicorn ASGI runner

```bash
uvicorn web.app:app --host 127.0.0.1 --port 8000 --reload
```

### Web Application URL

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 4. Web Application Structure

```text
web/
├── app.py                      # FastAPI application, route handlers & static mounts
├── README.md                   # Web platform documentation and developer guide
├── services/
│   ├── __init__.py
│   ├── analysis_service.py     # Cached CLIP model inference, contrast stretching & Bedrock abstraction
│   ├── lifecycle_service.py    # Storage tier placement, audit logging & S3 abstraction
│   └── analytics_service.py    # Dynamic CSV aggregation, KPI calculation & cost models
├── templates/
│   ├── base.html               # Master layout, navigation sidebar, modal & theme tokens
│   ├── dashboard.html          # Page 1: Dynamic KPI cards, Chart.js graphs & recent activity log
│   ├── analyze.html            # Page 2: Satellite image upload, sample picker & live CLIP inference
│   ├── archive.html            # Page 3: Searchable & filterable satellite archive browser
│   ├── analytics.html          # Page 4: Statistical distributions, histogram & cost optimization
│   └── architecture.html       # Page 5: Local prototype vs. Proposed AWS cloud deployment
├── static/
│   ├── css/
│   │   └── style.css           # Dark navy aerospace theme, responsive layout & custom components
│   ├── js/
│   │   └── app.js              # Chart.js renderers, inference lifecycle UI & search filters
│   └── images/
│       └── satellite_icon.png  # Satellite asset icon
└── uploads/                    # Temporary staging for user-uploaded satellite images
```

---

## 5. API Endpoints

The backend provides RESTful JSON endpoints alongside HTML views:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Dashboard page with dynamic KPIs and charts |
| `GET` | `/analyze` | Interactive Image Analysis and Inference page |
| `GET` | `/archive` | Satellite Image Archive Browser page |
| `GET` | `/analytics` | Deep-dive statistical and cost analytics page |
| `GET` | `/architecture` | Local Prototype vs Proposed AWS architecture page |
| `GET` | `/api/summary` | JSON summary: Total count, category breakdown, storage breakdown, average score |
| `GET` | `/api/analytics` | JSON datasets for Chart.js charts, histograms, and cost modeling |
| `GET` | `/api/images` | JSON archive list with query filters (`category`, `storage_class`, `search`) |
| `GET` | `/api/images/{filename}` | JSON detailed metadata for a single satellite image |
| `GET` | `/api/lifecycle` | JSON lifecycle audit log entries from `results/lifecycle_log.csv` |
| `GET` | `/api/samples` | JSON list of available sample TIFFs in `dataset/sample/` |
| `GET` | `/api/sample-preview/{filename}` | On-the-fly contrast-stretched JPEG preview for 16-bit GeoTIFFs |
| `POST` | `/api/analyze` | Multipart upload or sample selection for live CLIP inference |

---

## 6. How the CLIP Foundation Model is Used

1. **Model Loading & In-Memory Caching:**
   - The platform loads `openai/clip-vit-base-patch32` via Hugging Face `transformers`.
   - A singleton pattern in `LocalCLIPService` (`web/services/analysis_service.py`) ensures weights are cached in memory on startup, eliminating repeated model reloads on every user request.

2. **Satellite Contrast Stretching Preprocessing:**
   - Source satellite TIFF images typically possess narrow 16-bit dynamic ranges where raw values are clustered near 0.
   - `enhance_satellite_image()` stretches the min/max values of each color channel to `[0, 255]`.
   - The image is resized to `(224, 224)` RGB JPEG format, matching CLIP's vision transformer input dimensions.

3. **Zero-Shot Semantic Scoring:**
   - Three calibrated prompt embeddings are used:
     - `"important satellite image containing urban infrastructure"` (High)
     - `"moderately important satellite image"` (Medium)
     - `"unimportant satellite image with little useful information"` (Low)
   - Probabilities are extracted via softmax:
     $$\text{Score} = P(\text{High}) \times 100 + P(\text{Medium}) \times 50 + P(\text{Low}) \times 0$$

4. **Tier Classification:**
   - **HIGH** ($\ge 70.0$) $\rightarrow$ `S3_STANDARD`
   - **MEDIUM** ($\ge 40.0$) $\rightarrow$ `S3_STANDARD_IA`
   - **LOW** ($< 40.0$) $\rightarrow$ `S3_GLACIER`

---

## 7. Dynamic Data Loading (No Fake Statistics)

All statistics, tables, and charts on the web application are loaded dynamically from the actual project output files:

- **Metadata & Scores:** `results/importance_scores.csv`
- **Audit Logs:** `results/lifecycle_log.csv`
- **Processed Images:** `dataset/processed/`
- **Simulated Cloud Storage:** `cloud_simulation/S3_STANDARD/`, `cloud_simulation/S3_STANDARD_IA/`, and `cloud_simulation/S3_GLACIER/`

When a new image is analyzed through the web interface, the system can automatically update `cloud_simulation/` and record the decision into `results/lifecycle_log.csv` and `results/importance_scores.csv`, keeping the dashboard in live synchronization.

---

## 8. Future AWS Cloud Integration

The codebase uses clean abstractions to make migrating from local simulation to live AWS services seamless without altering UI controllers:

### Storage Service Abstraction (`BaseStorageService`):
- `LocalSimulationStorageService`: Reads/writes local simulation folders.
- `S3StorageService`: Prepared placeholder with environment variables:
  ```bash
  AWS_REGION="us-east-1"
  S3_BUCKET="satellite-archive-storage-2026"
  DYNAMODB_TABLE="SatelliteLifecycleMetadata"
  ```
  Switching between local simulation and AWS S3 requires only swapping the service binding in `web/services/lifecycle_service.py`.

### Vision Service Abstraction (`BaseVisionService`):
- `LocalCLIPService`: Executes PyTorch CLIP locally.
- `BedrockVisionService`: Prepared placeholder with environment variables:
  ```bash
  BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
  AWS_REGION="us-east-1"
  ```
  Allows swapping local PyTorch inference with managed AWS Bedrock or SageMaker endpoints.

# Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models (IntelliArchive)

**Course:** BCSE355L – Cloud Architecture Design  
**Project Phase:** Final Project Technical Report  
**Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore  
**Supervisor:** Dr. Priya V, Associate Professor  

### Project Authors
* **K. Pavan Kumar Reddy** — Registration No: `24BIT0580`
* **Anhad** — Registration No: `24BIT0129`

---

## 1. Executive Summary & Abstract

Modern Earth observation satellites collect immense volumes of multi-spectral imagery on a continuous basis. However, prevailing cloud object storage lifecycle mechanisms—such as native Amazon Web Services (AWS) S3 Lifecycle rules—operate in a content-blind fashion, relying exclusively on object creation age, directory prefix matching, or fixed transition schedules. This age-based paradigm leads to two acute operational failures:
1. **Premature Archival of High-Value Assets:** High-resolution imagery depicting critical transportation corridors, urban infrastructure, or active natural disasters is transitioned into cold archival tiers (e.g., S3 Glacier) simply because a time threshold elapsed, incurring punitive retrieval latencies and egress penalties when urgent analysis is needed.
2. **Unnecessary Hot Storage Expenditures:** Cloud-covered, sensor-degraded, or uninformative open-terrain imagery remains in expensive hot storage (S3 Standard @ $0.023/GB/month) for months before expiring.

**IntelliArchive** solves this problem by introducing content-aware cloud lifecycle optimization driven by Vision Foundation Models. By leveraging the zero-shot semantic capabilities of OpenAI CLIP ViT-B/32, satellite imagery is evaluated at ingestion time. A normalized composite score ($0 - 100$) dynamically categorizes each image into `HIGH`, `MEDIUM`, or `LOW` operational relevance, automatically mapping objects to optimal AWS S3 storage classes (`S3_STANDARD`, `S3_STANDARD_IA`, and `S3_GLACIER`).

The completed system features:
* A local multi-tier directory simulation with atomic file migrations and audit logging.
* Direct cloud integration with a private AWS S3 bucket in `ap-south-1` (Mumbai).
* An asynchronous FastAPI web platform with dark-mode dashboard, real-time CLIP inference, archive browser, and dynamic cost optimization analytics.
* A hardened, CPU-optimized Docker container (1.36 GB) successfully pushed to Amazon Elastic Container Registry (ECR).
* A 100% passing automated test suite covering 41 unit and integration test cases.

Empirical evaluation demonstrates projected monthly cloud storage cost savings of **up to 49.0%** while ensuring critical assets remain immediately accessible.

---

## 2. Problem Statement & Motivation

### 2.1 The Inefficiency of Static Time-Based Policies
Traditional cloud lifecycle configuration relies on policy blocks like the following:
```xml
<LifecycleConfiguration>
    <Rule>
        <ID>TransitionAfter90Days</ID>
        <Filter><Prefix>satellite-images/</Prefix></Filter>
        <Status>Enabled</Status>
        <Transitions>
            <Transition>
                <Days>90</Days>
                <StorageClass>STANDARD_IA</StorageClass>
            </Transition>
            <Transition>
                <Days>180</Days>
                <StorageClass>GLACIER</StorageClass>
            </Transition>
        </Transitions>
    </Rule>
</LifecycleConfiguration>
```
Under this policy:
* Every object matching the prefix is treated identically regardless of whether it contains dense city infrastructure or complete cloud obscuration.
* High-utility images transition into cold storage after 180 days, requiring 3–5 hours of Glacier retrieval time when needed for change detection or urban planning.
* Empty ocean or cloud scenes occupy expensive hot storage for half a year.

### 2.2 The Content-Aware Objective
The objective of IntelliArchive is to replace temporal assumptions with semantic value assessment, ensuring that storage tier placement reflects informational density and operational importance from the moment of ingestion.

---

## 3. System Architecture

IntelliArchive defines a dual-engine architecture: an implemented local prototype for reproducible academic demonstration and a proposed AWS cloud-native production deployment.

```
+-----------------------------------------------------------------------------------------+
|                                    INTELLIARCHIVE                                       |
+-----------------------------------------------------------------------------------------+
| LOCAL PROTOTYPE (Implemented & Tested)    | PROPOSED AWS PRODUCTION ARCHITECTURE        |
+-------------------------------------------+---------------------------------------------+
| • FastAPI Web Application (Uvicorn)       | • AWS ECS Fargate (Serverless Container)    |
| • PyTorch CLIP ViT-B/32 (Local CPU)       | • Amazon Bedrock (Claude 3.5 / Titan)       |
| • Local Tiers (cloud_simulation/*)        | • AWS S3 Intelligent-Tiering / Lifecycle    |
| • Atomic CSV Ledger (results/*.csv)       | • Amazon DynamoDB (Global Secondary Index)  |
| • Live AWS S3 Bucket (ap-south-1)         | • Multi-Region S3 Replication               |
| • Local AWS CLI Profile fallback          | • IAM Task Roles (Zero Hardcoded Keys)      |
+-------------------------------------------+---------------------------------------------+
```

### 3.1 Local Simulation Prototype
* **Directory Structure:** Emulates S3 storage classes locally:
  * `cloud_simulation/S3_STANDARD/`
  * `cloud_simulation/S3_STANDARD_IA/`
  * `cloud_simulation/S3_GLACIER/`
* **Atomic Migrations:** Moving an object across tiers atomically transfers the physical file and updates the audit ledgers, preventing orphaned files or duplicate entries.
* **Audit Ledgers:** 
  * `results/lifecycle_log.csv`: Transactional audit trail of tier movements.
  * `results/importance_scores.csv`: Historical database of evaluated imagery scores.

### 3.2 Real Amazon S3 Integration
* **Target Bucket:** `intelliarchive-pavan-satellite-2026`
* **AWS Region:** `ap-south-1` (Asia Pacific - Mumbai)
* **Access Model:** Private S3 bucket with Block Public Access enabled, accessed via scoped IAM identity `arn:aws:iam::371234372967:user/intelliarchive-app`.
* **Application Features:** Real-time object listing, pagination, and direct upload from the web interface.

---

## 4. Vision Foundation Model Methodology

```
┌─────────────────────────────────┐
│ Multi-Spectral Satellite GeoTIFF│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Dynamic Min-Max Percentile      │
│ Contrast Stretching [0, 255]    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Resize to 224 × 224 RGB         │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ OpenAI CLIP ViT-B/32 Transformer│
│ Zero-Shot Similarity Scoring    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Softmax Probabilities:          │
│ P(High), P(Medium), P(Low)      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Composite Importance Score      │
│ Score = (P_H×100) + (P_M×50)    │
└────────────────┬────────────────┘
                 │
   ┌─────────────┼─────────────┐
   │ ≥ 70        │ 40 - 69.9   │ < 40
   ▼             ▼             ▼
  HIGH         MEDIUM         LOW
S3_STANDARD S3_STANDARD_IA S3_GLACIER
```

### 4.1 Radiometric Preprocessing
Satellite sensors capture radiometric data with 16-bit depth. Because reflectance values are concentrated in low dynamic ranges, feeding raw data to models results in pure black images. `enhance_satellite_image()` stretches per-channel min and max values to the 8-bit dynamic range `[0, 255]`:

$$\text{Enhanced}_{c}(x, y) = \frac{\text{Pixel}_{c}(x, y) - \min(C)}{\max(C) - \min(C)} \times 255.0$$

The output is bilinearly interpolated to $224 \times 224$ pixels.

### 4.2 Zero-Shot Prompt Anchoring
Three prompt embeddings act as semantic reference anchors:
* **High Importance ($P_{\text{High}}$):** `"important satellite image containing urban infrastructure"`
* **Medium Importance ($P_{\text{Med}}$):** `"moderately important satellite image"`
* **Low Importance ($P_{\text{Low}}$):** `"unimportant satellite image with little useful information"`

### 4.3 Composite Scoring Formula
Cosine similarities are converted to normalized probabilities via softmax, and a composite score ($0 - 100$) is computed:

$$\text{Score} = (P_{\text{High}} \times 100) + (P_{\text{Med}} \times 50) + (P_{\text{Low}} \times 0)$$

### 4.4 Tier Assignment Policy
* **Score $\ge 70.0$ $\rightarrow$ `HIGH` $\rightarrow$ `S3_STANDARD`:** Immediate hot access; high-resolution buildings, roads, and infrastructure.
* **$40.0 \le \text{Score} < 70.0$ $\rightarrow$ `MEDIUM` $\rightarrow$ `S3_STANDARD_IA`:** Infrequent access tier; suburban, moderate-density scenes.
* **$\text{Score} < 40.0$ $\rightarrow$ `LOW` $\rightarrow$ `S3_GLACIER`:** Cold archival; barren desert, uninformative ocean, or heavy cloud cover.

---

## 5. Experimental Results & Cost Optimization

### 5.1 Dataset Evaluation
The system was evaluated against SpaceNet (Las Vegas AOI 2) high-resolution WorldView-3 satellite imagery. The scoring distribution clearly separated infrastructure-rich areas from sparse zones.

### 5.2 AWS S3 Pricing & Cost Comparison
Based on AWS Mumbai (`ap-south-1`) standard rates:
* **S3 Standard:** \$0.0230 per GB / month
* **S3 Standard-IA:** \$0.0125 per GB / month (45.6% cheaper)
* **S3 Glacier Flexible Retrieval:** \$0.0040 per GB / month (82.6% cheaper)

#### Simulation for a 10 TB Satellite Archive:

| Storage Strategy | Distribution | Monthly Cost | Projected Annual Savings |
|---|---|---|---|
| **Flat S3 Standard (Baseline)** | 100% S3 Standard | **\$230.00 / mo** | \$0.00 (Baseline) |
| **Traditional Time-Based Policy** | 60% Standard, 40% IA | **\$188.00 / mo** | \$504.00 / year (18.2% savings) |
| **IntelliArchive Content-Aware** | 25% Standard, 35% IA, 40% Glacier | **\$117.25 / mo** | **\$1,353.00 / year (49.0% savings)** |

---

## 6. Containerization & AWS ECR Deployment

### 6.1 Docker Image Optimization
Initial builds using standard PyTorch wheels produced ~12 GB images due to bundled CUDA runtime libraries. By explicitly installing the official CPU-only PyTorch wheels:
```dockerfile
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
```
and pre-caching CLIP weights during build, the final container image was reduced to **1.36 GB**.

### 6.2 Amazon ECR Verification
The optimized container was pushed to Amazon Elastic Container Registry:
* **Registry URI:** `371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive`
* **Pushed Tag:** `cpu-test` (Digest: `sha256:84466845b463ae57c754ec9d119403f4ed52ecc358b2612911cdd10f312e7df2`)
* **Status:** Verified and active in AWS.

---

## 7. Automated Test Verification

A test suite of **41 automated tests** was executed via `pytest`, achieving a **100% pass rate**:

1. **Storage Tiering (`tests/test_lifecycle_storage.py` - 10 tests):**
   - Validates acceptance of `S3_STANDARD`, `S3_STANDARD_IA`, and `S3_GLACIER`.
   - Rejects invalid storage class strings.
   - Enforces atomic multi-hop migrations without duplicate files.
   - Verifies CSV ledger consistency across re-classifications.
2. **AWS S3 Service (`tests/test_s3_service.py` - 24 tests):**
   - Validates upload success, custom object prefixes, and missing file handling.
   - Verifies paginated object listings and prefix filters.
   - Guarantees zero credentials leak into exception messages.
   - Verifies IAM Task Role resolution when running in containerized ECS environments.
3. **Web Application & APIs (`tests/test_web_app.py` - 7 tests):**
   - Verifies server-side HTML rendering across all 5 views.
   - Tests `/api/summary`, `/api/analytics`, and `/api/lifecycle` REST endpoints.
   - End-to-end inference verification via `/api/analyze-sample`.

---

## 8. Work Distribution & Team Contributions

| Team Member | Registration No. | Core Responsibilities & Technical Deliverables |
|---|---|---|
| **K. Pavan Kumar Reddy** | **24BIT0580** | • Cloud Architecture & S3 Storage Class tiering design.<br>• FastAPI Web Application, Aerospace UI, and Chart.js integration.<br>• AWS S3 service integration (`s3_service.py`) and IAM credential resolution.<br>• Dockerfile optimization (CPU wheels), build-time model caching, and Amazon ECR registry push management.<br>• Integration tests for AWS S3 service and web client. |
| **Anhad** | **24BIT0129** | • Vision Foundation Model pipeline (OpenAI CLIP ViT-B/32 zero-shot inference).<br>• Satellite radiometric image preprocessing (16-bit GeoTIFF contrast stretching).<br>• Local simulation storage directory engine and atomic CSV audit ledgers.<br>• AWS economic cost optimization model and storage lifecycle unit tests. |

---

## 9. Conclusion & Future Roadmap

**IntelliArchive** demonstrates the feasibility and economic advantages of content-aware cloud storage lifecycle management. By substituting static chronological rules with vision foundation model intelligence, storage costs can be halved while ensuring critical assets remain immediately accessible.

### Future Work:
1. **Amazon Bedrock:** Replace local model execution with cloud-native multimodal models (Claude 3.5 Sonnet / Amazon Titan) via the Bedrock API.
2. **Amazon DynamoDB:** Transition the CSV ledgers into a distributed DynamoDB table with global secondary indexes on semantic score and storage class.
3. **AWS EventBridge & Lambda:** Automate event-driven inference triggers whenever new satellite imagery lands in intake S3 buckets.

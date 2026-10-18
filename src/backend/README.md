# Backend Architecture

The backend services, business logic, and RESTful APIs for IntelliArchive are centralized in [`web/`](../../web/) and [`web/services/`](../../web/services/) for cohesive asynchronous operation:

- **API Entrypoint:** [`web/app.py`](../../web/app.py) — FastAPI ASGI web application serving dashboard endpoints, image analysis, archive browsing, and dynamic analytics.
- **Image Analysis Service:** [`web/services/analysis_service.py`](../../web/services/analysis_service.py) — Ingests satellite imagery, performs dynamic radiometric contrast stretching, executes zero-shot CLIP ViT-B/32 inference, and maps semantic scores to S3 storage classes.
- **Lifecycle Storage Service:** [`web/services/lifecycle_service.py`](../../web/services/lifecycle_service.py) — Manages atomic multi-hop file migrations across storage tiers and logs transactional entries to `results/lifecycle_log.csv`.
- **Cloud S3 Service:** [`web/services/s3_service.py`](../../web/services/s3_service.py) — Boto3 client wrapper communicating directly with the private AWS S3 bucket in `ap-south-1`.
- **Analytics Service:** [`web/services/analytics_service.py`](../../web/services/analytics_service.py) — Computes statistical distributions and evaluates the AWS storage cost optimization model.

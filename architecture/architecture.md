# IntelliArchive: System and Cloud Architecture

## Purpose and status

IntelliArchive is an academic prototype for content-aware lifecycle recommendations on satellite imagery. It combines a FastAPI web interface, local CLIP inference, local storage-tier simulation, and separate Amazon S3 list/upload functionality.

A recommendation is not yet an automatic cloud storage transition. The lifecycle service copies images into local simulation folders and updates CSV files. Its S3StorageService is a placeholder that raises NotImplementedError. The DynamoDB metadata table provisioned in AWS is not connected to this lifecycle path.

## Current application flow

Browser user
  -> HTTP request to FastAPI/Jinja2 web app on port 8080
  -> image validation and preview preparation
  -> CLIP ViT-B/32 inference in the application container
  -> probabilities and weighted importance score
  -> HIGH, MEDIUM, or LOW recommendation
  -> if archive is selected, local tier copy and CSV update

Separately: the archive page can list and upload objects to the configured private S3 bucket. That feature does not change an S3 object's storage class based on the recommendation.

## Analysis and lifecycle decision

1. The user selects a sample image or uploads a supported image through the analysis page.
2. The app validates the image and prepares a browser preview. Contrast stretching is for display, not radiometric calibration.
3. The inference pipeline prepares RGB input at 224 × 224 and runs CLIP ViT-B/32 against high-, medium-, and low-importance text prompts.
4. It combines softmax probabilities as: 100 × P(high) + 50 × P(medium) + 0 × P(low).
5. Current thresholds map scores >= 70 to HIGH / S3_STANDARD, scores >= 40 and < 70 to MEDIUM / S3_STANDARD_IA, and scores < 40 to LOW / S3_GLACIER.
6. When the user archives a result, the simulation copies the file to cloud_simulation/<tier>/ and updates results/lifecycle_log.csv and results/importance_scores.csv.

This prompt-dependent score is a proof-of-concept heuristic, not a validated measure of scientific or operational value. CLIP is not fine-tuned on the project dataset.

## Data persistence boundaries

| Data | Current location | Persistence behavior |
| --- | --- | --- |
| Working uploads and simulated tier copies | Application/container filesystem | Local to a task; may disappear after task replacement or restart |
| Lifecycle decisions and scores | results/lifecycle_log.csv and results/importance_scores.csv | Local files, not a shared durable database |
| Objects explicitly uploaded from S3 panel | Configured private S3 bucket | Durable S3 objects, independent of local simulation ledger |
| Container output | CloudWatch Logs | Retained according to log-group configuration |
| Lifecycle metadata | Provisioned DynamoDB table | Table exists, but application lifecycle service does not write to it |

For durable operation, keep imagery in S3 and decision metadata in DynamoDB or another managed database. Record object key, model and prompt version, probabilities, score, category, recommendation, transition status, and timestamps. Add idempotency and retry handling.

## AWS deployment architecture

Developer or build pipeline
  -> Amazon ECR stores the container image
  -> Amazon ECS on Fargate runs the FastAPI task
  -> IAM task role supplies AWS credentials to permitted calls
  -> CloudWatch Logs receives task output
  -> S3 is used for explicit archive-page listing and upload
  -> DynamoDB lifecycle writes are pending integration
  -> local folders and CSV files remain task-local simulation state

Fargate runs the container without user-managed EC2 hosts. The demo endpoint has been exposed over HTTP on port 8080; a task IP may change when tasks are replaced and is not a stable production URL.

CodeBuild builder setup was created, but the requested Linux/Medium concurrent-build quota was under AWS Support review in the last recorded project update. Do not claim a fully automated CI/CD pipeline unless that build has since succeeded.

## Target production workflow (not implemented end to end)

User upload -> persist source image in S3 -> run inference -> save decision and provenance to DynamoDB -> apply an approved S3 tier/tag policy -> record outcome -> emit structured logs and metrics -> return result to the user.

This target requires implementing S3 lifecycle actions and DynamoDB writes, then validating permissions, object tracking, retries, and audit records. Define whether transitions are automatic, policy-driven, or human-approved. Handle Standard-IA retrieval/minimum-duration costs and Glacier restore delays.

## Component status

| Component | Status | Boundary |
| --- | --- | --- |
| FastAPI dashboard and analysis | Implemented | Repository web application |
| CLIP ViT-B/32 inference and score | Implemented | CPU inference in application |
| Tier folders and CSV audit files | Implemented | Local simulation in web/services/lifecycle_service.py |
| S3 listing/upload | Implemented separately | web/services/s3_service.py; not a lifecycle transition |
| ECR, ECS/Fargate, CloudWatch | Deployed/configured for demo | Verify current task health before presentation |
| DynamoDB lifecycle writes | Pending integration | Table exists; lifecycle service does not write to it |
| CodeBuild image build | Pending quota approval in last update | AWS Support case was open |
| S3 class changes driven by CLIP | Not implemented | Do not present as completed |

## Recommended completion order

1. Confirm ECS task health, task-definition revision, image digest, and CloudWatch logs before the demo.
2. Move lifecycle metadata from CSV to DynamoDB, or clearly label CSV persistence as prototype-only; verify behavior after task replacement.
3. Implement S3 transition/tagging with least-privilege IAM, retries, object-key tracking, and an audit record.
4. Decide if transitions are immediate, policy-driven, or human-approved.
5. Add HTTPS, stable DNS/load balancing, health checks, alarms, and build automation after quota approval.
6. Run an end-to-end cloud demo and update this status table with dated evidence.

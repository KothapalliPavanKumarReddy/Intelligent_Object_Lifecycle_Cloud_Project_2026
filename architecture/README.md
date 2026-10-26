# IntelliArchive architecture

This folder separates the implementation that exists today from the production design still to be completed. See architecture.md for system flow, persistence boundaries, and the implementation roadmap.

## Current status at a glance

- The web app is FastAPI in a Docker container deployed as an ECS/Fargate task. CLIP inference runs inside the app container.
- Lifecycle decisions are copied into local simulation folders and recorded in CSV files.
- The archive page has separate Amazon S3 listing and upload functions. These do not perform the lifecycle service's storage-class transitions.
- The lifecycle service's S3StorageService is a placeholder. The application does not write lifecycle decisions to DynamoDB.
- ECS task logs are available through CloudWatch. The task filesystem is temporary; local folders and CSVs are not a durable shared ledger.

“Implemented” means present in source. “Deployed” means provisioned or observed in AWS, not necessarily used by every app feature. “Planned” means it still needs implementation and verification.

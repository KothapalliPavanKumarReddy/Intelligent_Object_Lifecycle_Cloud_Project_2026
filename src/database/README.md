# Database & Metadata Storage Design

IntelliArchive employs a dual metadata architecture supporting local prototyping and proposed cloud production:

### 1. Implemented Local Simulation Ledgers
The local prototype uses atomic CSV ledgers located in [`results/`](../../results/):
- **`lifecycle_log.csv`**: Transactional ledger recording object transitions:
  `timestamp,image_name,importance_score,category,source_storage_class,target_storage_class,status`
- **`importance_scores.csv`**: Evaluation registry maintaining image metadata, CLIP semantic probabilities, and final storage tier decisions.
- **Atomic Concurrency:** State updates are managed by [`LocalSimulationStorageService`](../../web/services/lifecycle_service.py) to prevent race conditions and eliminate orphaned files during multi-hop tier transitions.

### 2. Proposed AWS Production Database
In production cloud environments, CSV ledgers are replaced by **Amazon DynamoDB**:
- **Table Name:** `SatelliteLifecycleMetadata`
- **Partition Key:** `ImageId` (String / UUID)
- **Sort Key:** `Timestamp` (Number / Unix epoch)
- **Global Secondary Indexes (GSI):**
  - `GSI-StorageClass`: Query images currently residing in specific tiers (`S3_STANDARD`, `S3_STANDARD_IA`, `S3_GLACIER`).
  - `GSI-Category`: Fast retrieval of high-priority urban/disaster assets.
- **DynamoDB Streams:** Automatically trigger AWS Lambda functions when new records are written or updated.

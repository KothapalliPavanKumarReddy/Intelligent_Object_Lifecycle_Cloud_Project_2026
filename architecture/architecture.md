# Intelligent Object Lifecycle Optimization
## Cloud Architecture

## 1. Current Prototype Architecture

```text
                    Satellite Image Archive
                              |
                              v
                    +---------------------+
                    | Image Preprocessing |
                    | Resize to 224x224   |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | CLIP Vision         |
                    | Foundation Model    |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | Semantic Importance |
                    | Score               |
                    +----------+----------+
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
               LOW          MEDIUM         HIGH
                 |             |             |
                 v             v             v
          S3_GLACIER    S3_STANDARD_IA  S3_STANDARD
                 |             |             |
                 +-------------+-------------+
                               |
                               v
                    Lifecycle Decision Log
                               |
                               v
                         Results Dashboard

2. Proposed AWS Cloud Deployment

                         Satellite Image Archive
                                  |
                                  v
                         +------------------+
                         |   Amazon S3      |
                         |  Image Storage   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | AWS Lambda /     |
                         | Processing Layer |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Vision Model     |
                         | / SageMaker      |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Importance Score |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |             |             |
                    v             v             v
                  LOW          MEDIUM         HIGH
                    |             |             |
                    v             v             v
             S3 Glacier    S3 Standard-IA   S3 Standard
                    |             |             |
                    +-------------+-------------+
                                  |
                                  v
                       S3 Lifecycle Policies
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             CloudWatch                    SNS Alerts
                    |
                    v
              Monitoring /
               Reporting
| Component             | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| Amazon S3             | Store satellite image archives                      |
| AWS Lambda            | Trigger and coordinate processing                   |
| Amazon SageMaker      | Host or execute the vision-model inference workflow |
| S3 Lifecycle Policies | Manage storage-class transitions                    |
| Amazon CloudWatch     | Monitoring and logging                              |
| Amazon SNS            | Optional notifications                              |
| AWS IAM               | Access control and permissions                      |

3. Prototype-to-Cloud Mapping
| Current Prototype       | Proposed AWS Component              |
| ----------------------- | ----------------------------------- |
| `dataset/sample/`       | Amazon S3 input bucket              |
| `preprocessing.py`      | AWS Lambda / processing service     |
| CLIP inference          | SageMaker / model inference service |
| `importance_scores.csv` | S3 / database result storage        |
| `cloud_simulation/`     | Amazon S3 storage classes           |
| `s3_lifecycle.py`       | S3 Lifecycle configuration          |
| `lifecycle_log.csv`     | CloudWatch / S3 logs                |
| `dashboard.py`          | Cloud monitoring/reporting layer    |

4. Data Flow
Satellite Image
      |
      v
Preprocessing
      |
      v
CLIP Inference
      |
      v
Semantic Importance Score
      |
      v
Importance Category
      |
      v
Storage Tier Selection
      |
      v
Lifecycle Management
      |
      v
Monitoring and Dashboard



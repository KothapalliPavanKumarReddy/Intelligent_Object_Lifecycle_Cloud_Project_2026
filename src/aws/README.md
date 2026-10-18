# AWS Cloud Architecture & Deployment Resources

This directory contains cloud architecture documentation, deployment templates, and service configurations for AWS cloud execution.

---

## ☁️ Active AWS Resources

| Resource | Identifier / ARN | Region | Status |
|---|---|---|---|
| **Amazon S3 Bucket** | `intelliarchive-pavan-satellite-2026` | `ap-south-1` | **Active & Private** (Block Public Access Enabled) |
| **Amazon ECR Repository** | `371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive` | `ap-south-1` | **Active** |
| **Container Image in ECR** | Tag: `cpu-test` (1.36 GB CPU-optimized PyTorch image) | `ap-south-1` | **Pushed & Verified** |
| **IAM Application User** | `arn:aws:iam::371234372967:user/intelliarchive-app` | `ap-south-1` | **Configured** (Least-privilege S3/ECR access) |

---

## 🚀 AWS Service Integrations

1. **Amazon S3 Client Service:**
   - Implemented in [`web/services/s3_service.py`](../../web/services/s3_service.py).
   - Manages direct multi-part image uploads to prefix `satellite-images/`.
   - Resolves local credentials via named profile `intelliarchive` or ECS Task Roles when `AWS_PROFILE=""`.

2. **AWS ECS / Fargate Serverless Deployment:**
   - Container Task Definition: [`ecs-task-definition.json`](./ecs-task-definition.json).
   - Deployment automation script: [`deploy_ecs.ps1`](./deploy_ecs.ps1).

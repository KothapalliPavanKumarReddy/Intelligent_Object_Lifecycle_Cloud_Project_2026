# ============================================================================
# IntelliArchive - Dockerfile for AWS ECS / Fargate Deployment
# ============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8080 \
    TORCH_HOME=/app/.cache/torch \
    HF_HOME=/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/app/.cache/huggingface/hub

# Set working directory inside container
WORKDIR /app

# Install minimal OS runtime dependencies (curl for healthchecks, libgomp1 for PyTorch/OpenMP)
# and clean up apt caches to minimize image layer size
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage Docker layer caching.
# Install CPU-only PyTorch & torchvision from the official PyTorch CPU wheel repository first.
# This prevents pulling ~5 GB of unused CUDA/NVIDIA runtime libraries onto CPU-only ECS Fargate.
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download and cache CLIP ViT-B/32 weights during image build.
# This prevents network dependency and download delays during ECS Fargate cold starts.
# HF_HUB_DISABLE_XET=1 bypasses the Xet storage backend (CAS Client errors).
# OPENSSL_CONF override lowers the TLS security level for the download only,
# working around CDN certificates rejected at the default SECLEVEL=2.
RUN printf '%s\n' \
      'import time, sys' \
      'from huggingface_hub import snapshot_download' \
      'model_id = "openai/clip-vit-base-patch32"' \
      'for attempt in range(1, 4):' \
      '    try:' \
      '        print(f"Downloading {model_id} (attempt {attempt}/3)...")' \
      '        snapshot_download(model_id, ignore_patterns=["*.h5", "*.msgpack"])' \
      '        print("Download complete.")' \
      '        break' \
      '    except Exception as e:' \
      '        print(f"Attempt {attempt} failed: {e}", file=sys.stderr)' \
      '        if attempt == 3:' \
      '            raise' \
      '        time.sleep(10)' \
      > /tmp/download_model.py \
    && printf '[openssl_init]\nssl_conf = ssl_sect\n[ssl_sect]\nsystem_default = system_default_sect\n[system_default_sect]\nCipherString = DEFAULT@SECLEVEL=1\n' > /tmp/openssl_seclevel1.cnf \
    && HF_HUB_DISABLE_XET=1 OPENSSL_CONF=/tmp/openssl_seclevel1.cnf python3 /tmp/download_model.py \
    && rm /tmp/download_model.py /tmp/openssl_seclevel1.cnf

# Copy application and dataset files needed by the web UI and services
COPY web/ /app/web/
COPY dataset/sample/ /app/dataset/sample/
COPY dataset/processed/ /app/dataset/processed/
COPY cloud_simulation/ /app/cloud_simulation/
COPY results/ /app/results/

# Create runtime directory structure and configure unprivileged user for security
RUN mkdir -p /app/web/uploads \
             /app/cloud_simulation/S3_STANDARD \
             /app/cloud_simulation/S3_STANDARD_IA \
             /app/cloud_simulation/S3_GLACIER \
             /app/results \
             /app/.cache && \
    useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to unprivileged user
USER appuser

# Expose target application port
EXPOSE 8080

# Container healthcheck for ECS Target Groups and local verification
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start FastAPI application via Uvicorn listening on 0.0.0.0:8080
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

import io
import os
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from web.services.analysis_service import clip_service, enhance_satellite_image
from web.services.lifecycle_service import lifecycle_service
from web.services.analytics_service import analytics_service
from web.services.s3_service import s3_service

# Project root dynamically resolved
PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = PROJECT_ROOT / "web"
TEMPLATES_DIR = WEB_DIR / "templates"
STATIC_DIR = WEB_DIR / "static"
UPLOADS_DIR = WEB_DIR / "uploads"
DATASET_PROCESSED_DIR = PROJECT_ROOT / "dataset" / "processed"
DATASET_SAMPLE_DIR = PROJECT_ROOT / "dataset" / "sample"
CLOUD_SIM_DIR = PROJECT_ROOT / "cloud_simulation"
RESULTS_DIR = PROJECT_ROOT / "results"

# Ensure all essential directories exist
for folder in [UPLOADS_DIR, DATASET_PROCESSED_DIR, DATASET_SAMPLE_DIR, CLOUD_SIM_DIR, RESULTS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit for satellite TIFFs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up cached resources and initialize environment on server startup."""
    print("=" * 60)
    print("Starting IntelliArchive Web Platform...")
    print(f"Project root: {PROJECT_ROOT}")
    print("Initializing local CLIP Vision Foundation Model...")
    try:
        clip_service.load_model()
        print("CLIP Model successfully initialized.")
    except Exception as e:
        print(f"Notice: CLIP Model will be loaded on first inference: {e}")
    print("=" * 60)
    yield
    print("IntelliArchive Web Platform shutting down...")


app = FastAPI(
    title="IntelliArchive",
    description="AI-Powered Satellite Object Lifecycle Optimization for Satellite Image Archives",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static and file directories
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if DATASET_SAMPLE_DIR.exists():
    app.mount("/images/sample", StaticFiles(directory=str(DATASET_SAMPLE_DIR)), name="sample_images")

if CLOUD_SIM_DIR.exists():
    app.mount("/images/storage", StaticFiles(directory=str(CLOUD_SIM_DIR)), name="cloud_storage")

if UPLOADS_DIR.exists():
    app.mount("/images/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploaded_images")

if RESULTS_DIR.exists():
    app.mount("/images/results", StaticFiles(directory=str(RESULTS_DIR)), name="results_images")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ============================================================================
# PAGE ROUTES (HTML)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Page 1 — Executive Dashboard with dynamic KPIs, charts, and activity log."""
    summary = analytics_service.get_summary_metrics()
    lifecycle_log = lifecycle_service.get_lifecycle_log()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "Dashboard",
            "active_page": "dashboard",
            "summary": summary,
            "lifecycle_log": lifecycle_log[:15]  # Most recent 15 records
        }
    )


@app.get("/analyze", response_class=HTMLResponse)
async def analyze_page(request: Request):
    """Page 2 — Interactive Satellite Image Analysis & Inference."""
    # List sample files from dataset/sample for quick testing
    sample_files = []
    if DATASET_SAMPLE_DIR.exists():
        for tiff in sorted(DATASET_SAMPLE_DIR.glob("*.tif")):
            sample_files.append(tiff.name)

    return templates.TemplateResponse(
        request=request,
        name="analyze.html",
        context={
            "page_title": "Analyze Image",
            "active_page": "analyze",
            "sample_files": sample_files
        }
    )


@app.get("/archive", response_class=HTMLResponse)
async def archive_page(
    request: Request,
    category: Optional[str] = Query(None),
    storage_class: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Page 3 — Satellite Image Archive Browser with filtering and detail inspection."""
    items = analytics_service.get_archive_items(category=category, storage_class=storage_class, search=search)
    summary = analytics_service.get_summary_metrics()
    return templates.TemplateResponse(
        request=request,
        name="archive.html",
        context={
            "page_title": "Archive Browser",
            "active_page": "archive",
            "items": items,
            "summary": summary,
            "current_category": category or "ALL",
            "current_storage": storage_class or "ALL",
            "current_search": search or ""
        }
    )


@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    """Page 4 — Deep-dive statistical analysis and cloud cost optimization."""
    summary = analytics_service.get_summary_metrics()
    cost_model = analytics_service.calculate_cost_savings()
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "page_title": "Analytics & Optimization",
            "active_page": "analytics",
            "summary": summary,
            "cost_model": cost_model
        }
    )


@app.get("/architecture", response_class=HTMLResponse)
async def architecture_page(request: Request):
    """Page 5 — Visual system architecture (Local Prototype vs Proposed AWS Cloud)."""
    return templates.TemplateResponse(
        request=request,
        name="architecture.html",
        context={
            "page_title": "System Architecture",
            "active_page": "architecture"
        }
    )


# ============================================================================
# API ENDPOINTS (JSON)
# ============================================================================

@app.get("/api/summary")
async def api_summary():
    """Retrieve system KPIs and storage distribution metrics."""
    return analytics_service.get_summary_metrics()


@app.get("/api/analytics")
async def api_analytics():
    """Retrieve complete data series for charts, histogram, and cost modeling."""
    summary = analytics_service.get_summary_metrics()
    charts = analytics_service.get_chart_data()
    cost_model = analytics_service.calculate_cost_savings()
    return {
        "summary": summary,
        "charts": charts,
        "cost_model": cost_model
    }


@app.get("/api/images")
async def api_images(
    category: Optional[str] = Query(None),
    storage_class: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Retrieve list of archived satellite images matching filter criteria."""
    items = analytics_service.get_archive_items(
        category=category,
        storage_class=storage_class,
        search=search
    )
    return {
        "count": len(items),
        "items": items
    }


@app.get("/api/images/{filename}")
async def api_image_detail(filename: str):
    """Retrieve complete metadata and lifecycle status for a specific image."""
    sanitized = Path(filename).name
    detail = analytics_service.get_image_details(sanitized)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Image '{sanitized}' not found in archive.")
    return detail


@app.get("/api/lifecycle")
async def api_lifecycle():
    """Retrieve all logged lifecycle decisions."""
    records = lifecycle_service.get_lifecycle_log()
    return {
        "total_records": len(records),
        "records": records
    }


@app.get("/api/samples")
async def api_samples():
    """List available sample raw TIFF images in repository."""
    sample_files = []
    if DATASET_SAMPLE_DIR.exists():
        for tiff in sorted(DATASET_SAMPLE_DIR.glob("*.tif")):
            sz_mb = round(tiff.stat().st_size / (1024 * 1024), 2)
            sample_files.append({
                "name": tiff.name,
                "size_mb": sz_mb
            })
    return {"samples": sample_files}


@app.get("/api/sample-preview/{filename}")
async def api_sample_preview(filename: str):
    """
    On-the-fly contrast stretching and preview generator for satellite TIFFs.
    Browsers cannot natively render 16-bit GeoTIFFs, so we generate a responsive JPEG preview.
    """
    sanitized = Path(filename).name
    sample_path = DATASET_SAMPLE_DIR / sanitized

    if not sample_path.exists():
        raise HTTPException(status_code=404, detail=f"Sample TIFF '{sanitized}' not found.")

    try:
        with Image.open(sample_path) as img:
            enhanced = enhance_satellite_image(img.convert("RGB"))
            # Resize for responsive web preview
            enhanced.thumbnail((800, 800), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            enhanced.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)
            return Response(content=buffer.getvalue(), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate preview: {str(e)}")


@app.get("/api/thumbnail/{filename}")
@app.get("/images/processed/{filename}")
async def api_thumbnail(filename: str):
    """
    Serve reliable contrast-stretched satellite imagery for archive and dashboard thumbnails.
    Uses the original GeoTIFF when available (matching the Analyze Image page visualization),
    or falls back to the processed JPEG asset.
    """
    sanitized = Path(filename).name
    # Extract base stem by stripping standard suffixes
    base_stem = sanitized.replace("_processed.jpg", "").replace(".jpg", "").replace(".tif", "").replace(".tiff", "")
    sample_path = DATASET_SAMPLE_DIR / f"{base_stem}.tif"

    # 1. If original GeoTIFF exists, serve using the reliable contrast-stretched preview
    if sample_path.exists():
        return await api_sample_preview(sample_path.name)

    # 2. Check if file exists in dataset/processed
    proc_path = DATASET_PROCESSED_DIR / sanitized
    if not proc_path.exists():
        proc_path = DATASET_PROCESSED_DIR / f"{base_stem}_processed.jpg"

    if proc_path.exists():
        try:
            with Image.open(proc_path) as img:
                enhanced = enhance_satellite_image(img.convert("RGB"))
                buffer = io.BytesIO()
                enhanced.save(buffer, format="JPEG", quality=90)
                buffer.seek(0)
                return Response(content=buffer.getvalue(), media_type="image/jpeg")
        except Exception:
            with open(proc_path, "rb") as f:
                return Response(content=f.read(), media_type="image/jpeg")

    # 3. Check cloud simulation storage
    if CLOUD_SIM_DIR.exists():
        for tier_dir in CLOUD_SIM_DIR.iterdir():
            if tier_dir.is_dir():
                candidate = tier_dir / sanitized
                if candidate.exists():
                    try:
                        with Image.open(candidate) as img:
                            enhanced = enhance_satellite_image(img.convert("RGB"))
                            buffer = io.BytesIO()
                            enhanced.save(buffer, format="JPEG", quality=90)
                            buffer.seek(0)
                            return Response(content=buffer.getvalue(), media_type="image/jpeg")
                    except Exception:
                        with open(candidate, "rb") as f:
                            return Response(content=f.read(), media_type="image/jpeg")

    raise HTTPException(status_code=404, detail=f"Image asset '{sanitized}' not found.")


@app.post("/api/analyze")
async def api_analyze(
    file: Optional[UploadFile] = File(None),
    sample_filename: Optional[str] = Form(None),
    save_to_simulation: bool = Form(True)
):
    """
    Analyze satellite image using cached CLIP Vision Foundation Model.
    Supports either an uploaded file (TIFF, PNG, JPG) OR a selected repository sample TIFF.
    """
    input_bytes: Optional[bytes] = None
    input_name: str = ""

    # 1. Handle uploaded file
    if file and file.filename:
        filename = Path(file.filename).name
        ext = Path(filename).suffix.lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty (0 bytes)."
            )

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds maximum size of {MAX_FILE_SIZE // (1024*1024)}MB."
            )

        input_bytes = contents
        input_name = filename

        # Save upload copy
        upload_dest = UPLOADS_DIR / filename
        with open(upload_dest, "wb") as f:
            f.write(contents)

    # 2. Or handle sample filename from dataset/sample
    elif sample_filename:
        sample_path = DATASET_SAMPLE_DIR / Path(sample_filename).name
        if not sample_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Sample file '{sample_filename}' not found."
            )
        input_name = sample_path.name
        with open(sample_path, "rb") as f:
            input_bytes = f.read()

    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide an image file to upload or select a repository sample."
        )

    # 3. Execute inference using cached CLIP service
    try:
        # Determine processed filename (e.g. img123_processed.jpg)
        base_stem = Path(input_name).stem
        processed_filename = f"{base_stem}_processed.jpg"
        processed_output_path = DATASET_PROCESSED_DIR / processed_filename

        analysis_result = clip_service.analyze_image(
            image_input=input_bytes,
            filename=processed_filename,
            save_processed_to=processed_output_path
        )

        # 4. Apply lifecycle action to local simulation if requested
        if save_to_simulation:
            lifecycle_record = lifecycle_service.store_and_apply_lifecycle(
                image_name=processed_filename,
                source_path=processed_output_path,
                score=analysis_result["importance_score"],
                category=analysis_result["category"],
                storage_class=analysis_result["storage_class"]
            )
            analysis_result["lifecycle_record"] = lifecycle_record

        analysis_result["processed_image_url"] = f"/images/processed/{processed_filename}"
        analysis_result["original_filename"] = input_name

        return JSONResponse(status_code=200, content=analysis_result)

    except Exception as e:
        print(f"Inference error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI model inference failed: {str(e)}"
        )


@app.get("/api/s3/objects")
async def api_s3_objects():
    """List images in the private AWS S3 bucket."""
    try:
        result = s3_service.list_objects(prefix="satellite-images/")
        if not result.get("success"):
            raise HTTPException(
                status_code=502,
                detail=result.get("error", "S3 listing failed"),
            )
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AWS S3 service error: {str(exc)}",
        )


@app.post("/api/s3/upload/{filename}")
async def api_s3_upload(filename: str):
    """Upload a processed image to private S3 storage."""
    sanitized = Path(filename).name
    if sanitized != filename or sanitized in ("", ".", ".."):
        raise HTTPException(status_code=400, detail="Invalid filename")

    source_path = DATASET_PROCESSED_DIR / sanitized
    if not source_path.is_file():
        # Fallback 1: check cloud simulation tier folders
        found = False
        for tier_name in ["S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"]:
            candidate = CLOUD_SIM_DIR / tier_name / sanitized
            if candidate.is_file():
                source_path = candidate
                found = True
                break
        # Fallback 2: check uploads folder
        if not found:
            candidate_upload = UPLOADS_DIR / sanitized
            if candidate_upload.is_file():
                source_path = candidate_upload
                found = True
        if not found:
            raise HTTPException(status_code=404, detail="Processed image not found")

    try:
        result = s3_service.upload_file(source_path)
        if not result.get("success"):
            raise HTTPException(
                status_code=502,
                detail=result.get("error", "S3 upload failed"),
            )
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AWS S3 upload error: {str(exc)}",
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=True)

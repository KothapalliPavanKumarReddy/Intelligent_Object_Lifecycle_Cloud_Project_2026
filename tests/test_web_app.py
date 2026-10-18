import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)


def test_html_pages():
    """Verify all 5 primary user-facing HTML pages render with 200 OK."""
    pages = ["/", "/analyze", "/archive", "/analytics", "/architecture"]
    for page in pages:
        res = client.get(page)
        assert res.status_code == 200, f"Route {page} returned {res.status_code}"
        assert "<html" in res.text.lower()


def test_api_summary():
    """Verify summary API returns correct dynamic metrics without hardcoded numbers."""
    res = client.get("/api/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_images" in data
    assert "categories" in data
    assert "storage_classes" in data
    assert "HIGH" in data["categories"]
    assert "MEDIUM" in data["categories"]
    assert "LOW" in data["categories"]
    assert "S3_STANDARD" in data["storage_classes"]
    assert "S3_STANDARD_IA" in data["storage_classes"]
    assert "S3_GLACIER" in data["storage_classes"]
    assert data["total_images"] > 0
    print(f"Summary dynamically loaded: total_images={data['total_images']}")


def test_api_analytics():
    """Verify analytics API returns complete chart data structures."""
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.json()
    assert "charts" in data
    assert "score_chart" in data["charts"]
    assert "category_chart" in data["charts"]
    assert "storage_chart" in data["charts"]
    assert "histogram_chart" in data["charts"]
    assert "cost_model" in data


def test_api_images_and_filters():
    """Verify image list retrieval and filtering."""
    res = client.get("/api/images")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] > 0
    first_item = data["items"][0]
    first_name = first_item["image_name"]

    # Detail API
    res_detail = client.get(f"/api/images/{first_name}")
    assert res_detail.status_code == 200
    assert res_detail.json()["image_name"] == first_name

    # Filter by category
    res_high = client.get("/api/images?category=HIGH")
    assert res_high.status_code == 200
    for item in res_high.json()["items"]:
        assert item["category"] == "HIGH"


def test_api_lifecycle():
    """Verify lifecycle log API returns entries."""
    res = client.get("/api/lifecycle")
    assert res.status_code == 200
    data = res.json()
    assert data["total_records"] > 0


def test_api_samples_and_preview():
    """Verify sample listing and GeoTIFF contrast-stretched preview generation."""
    res = client.get("/api/samples")
    assert res.status_code == 200
    data = res.json()
    assert len(data["samples"]) > 0
    sample_name = data["samples"][0]["name"]

    # Request preview
    res_preview = client.get(f"/api/sample-preview/{sample_name}")
    assert res_preview.status_code == 200
    assert res_preview.headers["content-type"] == "image/jpeg"
    assert len(res_preview.content) > 1000  # Valid non-empty JPEG


def test_api_analyze_sample():
    """Verify real AI inference pipeline using cached CLIP foundation model."""
    res_samples = client.get("/api/samples")
    sample_name = res_samples.json()["samples"][0]["name"]

    # Run inference via POST /api/analyze with sample_filename
    res_analyze = client.post(
        "/api/analyze",
        data={
            "sample_filename": sample_name,
            "save_to_simulation": "false"  # Read-only test
        }
    )
    assert res_analyze.status_code == 200
    data = res_analyze.json()
    assert "importance_score" in data
    assert 0 <= data["importance_score"] <= 100
    assert data["category"] in ["HIGH", "MEDIUM", "LOW"]
    assert data["storage_class"] in ["S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"]
    assert data["model"] == "openai/clip-vit-base-patch32"
    assert data["status"] == "Analysis Complete"
    print(f"Test inference output for {sample_name}: score={data['importance_score']}, category={data['category']}, storage={data['storage_class']}")


def test_api_analyze_empty_file_rejected():
    """Verify empty 0-byte upload is cleanly rejected with HTTP 400."""
    res = client.post(
        "/api/analyze",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
        data={"save_to_simulation": "false"}
    )
    assert res.status_code == 400
    assert "empty" in res.json()["detail"].lower()


def test_api_thumbnail_endpoint():
    """Verify thumbnail endpoint handles requests cleanly."""
    res = client.get("/api/thumbnail/nonexistent_image.jpg")
    assert res.status_code == 404

    # Existing sample TIFF thumbnail
    res_samples = client.get("/api/samples")
    sample_name = res_samples.json()["samples"][0]["name"]
    res_thumb = client.get(f"/api/thumbnail/{sample_name}")
    assert res_thumb.status_code == 200
    assert res_thumb.headers["content-type"] == "image/jpeg"


def test_api_s3_upload_missing_file():
    """Verify S3 upload returns 404 if file is absent from all local storage folders."""
    res = client.post("/api/s3/upload/definitely_missing_12345.jpg")
    assert res.status_code == 404


if __name__ == "__main__":
    print("Running IntelliArchive Test Suite...")
    test_html_pages()
    print(" [PASS] test_html_pages")
    test_api_summary()
    print(" [PASS] test_api_summary")
    test_api_analytics()
    print(" [PASS] test_api_analytics")
    test_api_images_and_filters()
    print(" [PASS] test_api_images_and_filters")
    test_api_lifecycle()
    print(" [PASS] test_api_lifecycle")
    test_api_samples_and_preview()
    print(" [PASS] test_api_samples_and_preview")
    test_api_analyze_sample()
    print(" [PASS] test_api_analyze_sample")
    test_api_analyze_empty_file_rejected()
    print(" [PASS] test_api_analyze_empty_file_rejected")
    test_api_thumbnail_endpoint()
    print(" [PASS] test_api_thumbnail_endpoint")
    test_api_s3_upload_missing_file()
    print(" [PASS] test_api_s3_upload_missing_file")
    print("\nALL 10 TESTS PASSED SUCCESSFULLY!")

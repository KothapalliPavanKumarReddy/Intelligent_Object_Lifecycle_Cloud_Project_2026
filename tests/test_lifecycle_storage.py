import sys, shutil
from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _make_lifecycle_service(tmp_path):
    import web.services.lifecycle_service as mod
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    cloud_dir = tmp_path / "cloud_simulation"
    storage_dirs = {
        "S3_STANDARD": cloud_dir / "S3_STANDARD",
        "S3_STANDARD_IA": cloud_dir / "S3_STANDARD_IA",
        "S3_GLACIER": cloud_dir / "S3_GLACIER",
    }
    for p in storage_dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    results_file = results_dir / "importance_scores.csv"
    log_file = results_dir / "lifecycle_log.csv"
    mod.RESULTS_FILE = results_file
    mod.LOG_FILE = log_file
    mod.STORAGE_DIRS = storage_dirs
    mod.SUPPORTED_TIERS = frozenset(storage_dirs.keys())
    svc = mod.LocalSimulationStorageService.__new__(mod.LocalSimulationStorageService)
    mod.LocalSimulationStorageService.__init__(svc)
    return svc, mod, storage_dirs, results_file, log_file


def _make_analytics_service(tmp_path, storage_dirs, results_file, log_file):
    import web.services.analytics_service as amod
    amod.RESULTS_FILE = results_file
    amod.LOG_FILE = log_file
    amod.PROCESSED_DIR = tmp_path / "dataset" / "processed"
    amod.SAMPLE_DIR = tmp_path / "dataset" / "sample"
    amod._STORAGE_DIRS = storage_dirs
    return amod.AnalyticsService()


def _dummy(path, content=b"FAKE"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


# --- Test 1: Invalid storage class rejected ---

def test_invalid_storage_class_is_rejected(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    source = tmp_path / "img_fake.jpg"
    _dummy(source)
    result = svc.store_and_apply_lifecycle(
        image_name="img_fake.jpg", source_path=source,
        score=75.0, category="HIGH", storage_class="S3_DEEP_ARCHIVE",
    )
    assert "error" in result
    assert result["status_code"] == 400
    assert "S3_DEEP_ARCHIVE" in result["error"]
    assert not log_file.exists()
    assert not results_file.exists()


def test_all_three_valid_tiers_are_accepted(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    for tier in ("S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"):
        img = f"img_{tier}.jpg"
        source = tmp_path / img
        _dummy(source)
        result = svc.store_and_apply_lifecycle(
            image_name=img, source_path=source,
            score=50.0, category="MEDIUM", storage_class=tier,
        )
        assert "error" not in result, f"Tier {tier} should be accepted"
        assert result["storage_class"] == tier


# --- Test 2: Missing source image rejected ---

def test_missing_source_image_returns_error(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    ghost = tmp_path / "nonexistent.jpg"
    assert not ghost.exists()
    result = svc.store_and_apply_lifecycle(
        image_name="nonexistent.jpg", source_path=ghost,
        score=60.0, category="MEDIUM", storage_class="S3_STANDARD",
    )
    assert "error" in result
    assert result["status_code"] == 404
    assert "nonexistent.jpg" in result["error"]
    for tier_path in storage_dirs.values():
        assert not (tier_path / "nonexistent.jpg").exists()
    assert not log_file.exists()
    assert not results_file.exists()


# --- Test 3: Tier change removes stale copies ---

def test_tier_change_removes_stale_copies(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    img = "img_transition.jpg"
    source = tmp_path / img
    _dummy(source)
    svc.store_and_apply_lifecycle(img, source, 80.0, "HIGH", "S3_STANDARD")
    assert (storage_dirs["S3_STANDARD"] / img).exists()
    svc.store_and_apply_lifecycle(img, source, 20.0, "LOW", "S3_GLACIER")
    assert (storage_dirs["S3_GLACIER"] / img).exists()
    assert not (storage_dirs["S3_STANDARD"] / img).exists()
    assert not (storage_dirs["S3_STANDARD_IA"] / img).exists()


def test_three_hop_tier_change(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    img = "img_threehop.jpg"
    source = tmp_path / img
    _dummy(source)
    for tier in ("S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"):
        svc.store_and_apply_lifecycle(img, source, 30.0, "LOW", tier)
    assert (storage_dirs["S3_GLACIER"] / img).exists()
    assert not (storage_dirs["S3_STANDARD"] / img).exists()
    assert not (storage_dirs["S3_STANDARD_IA"] / img).exists()


# --- Test 4: No duplicate CSV records ---

def test_no_duplicate_rows_after_multiple_stores(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    img = "img_dup.jpg"
    source = tmp_path / img
    _dummy(source)
    svc.store_and_apply_lifecycle(img, source, 70.0, "HIGH", "S3_STANDARD")
    svc.store_and_apply_lifecycle(img, source, 30.0, "LOW", "S3_GLACIER")
    svc.store_and_apply_lifecycle(img, source, 50.0, "MEDIUM", "S3_STANDARD_IA")
    df_scores = pd.read_csv(results_file)
    df_log = pd.read_csv(log_file)
    assert df_scores["image_name"].tolist().count(img) == 1
    assert df_log["image_name"].tolist().count(img) == 1
    assert df_scores[df_scores["image_name"] == img]["storage_class"].iloc[0] == "S3_STANDARD_IA"
    assert df_log[df_log["image_name"] == img]["storage_class"].iloc[0] == "S3_STANDARD_IA"


def test_multiple_images_no_cross_contamination(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    images = [("img_a.jpg", 90.0, "HIGH", "S3_STANDARD"),
              ("img_b.jpg", 50.0, "MEDIUM", "S3_STANDARD_IA"),
              ("img_c.jpg", 10.0, "LOW", "S3_GLACIER")]
    for name, score, cat, tier in images:
        src = tmp_path / name
        _dummy(src)
        svc.store_and_apply_lifecycle(name, src, score, cat, tier)
    df_scores = pd.read_csv(results_file)
    df_log = pd.read_csv(log_file)
    assert len(df_scores) == 3
    assert len(df_log) == 3
    assert set(df_scores["image_name"]) == {"img_a.jpg", "img_b.jpg", "img_c.jpg"}


# --- Test 5: Analytics ground-truth tier detection ---

def test_analytics_reports_actual_tier_not_stale_csv(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    analytics = _make_analytics_service(tmp_path, storage_dirs, results_file, log_file)
    img = "img_stale.jpg"
    source = tmp_path / img
    _dummy(source)
    svc.store_and_apply_lifecycle(img, source, 80.0, "HIGH", "S3_STANDARD")
    shutil.move(str(storage_dirs["S3_STANDARD"] / img), str(storage_dirs["S3_GLACIER"] / img))
    items = analytics.get_archive_items()
    assert len(items) == 1
    item = items[0]
    assert item["actual_storage_tier"] == "S3_GLACIER"
    assert item["storage_class"] == "S3_GLACIER"
    assert item["exists_in_cloud"] is True
    assert item["missing_from_cloud"] is False


def test_analytics_detects_missing_file(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    analytics = _make_analytics_service(tmp_path, storage_dirs, results_file, log_file)
    img = "img_missing.jpg"
    source = tmp_path / img
    _dummy(source)
    svc.store_and_apply_lifecycle(img, source, 55.0, "MEDIUM", "S3_STANDARD_IA")
    (storage_dirs["S3_STANDARD_IA"] / img).unlink()
    items = analytics.get_archive_items()
    assert len(items) == 1
    item = items[0]
    assert item["exists_in_cloud"] is False
    assert item["missing_from_cloud"] is True
    assert item["actual_storage_tier"] is None
    assert item["lifecycle_status"] == "Preprocessed"


# --- Test 6: CSV consistency across tier changes ---

def test_csvs_stay_consistent_across_tier_changes(tmp_path):
    svc, mod, storage_dirs, results_file, log_file = _make_lifecycle_service(tmp_path)
    img = "img_sync.jpg"
    source = tmp_path / img
    _dummy(source)
    for tier in ("S3_STANDARD", "S3_GLACIER", "S3_STANDARD_IA"):
        svc.store_and_apply_lifecycle(img, source, 50.0, "MEDIUM", tier)
        df_s = pd.read_csv(results_file)
        df_l = pd.read_csv(log_file)
        tier_in_scores = df_s[df_s["image_name"] == img]["storage_class"].iloc[0]
        tier_in_log = df_l[df_l["image_name"] == img]["storage_class"].iloc[0]
        assert tier_in_scores == tier, f"importance_scores.csv shows {tier_in_scores}"
        assert tier_in_log == tier, f"lifecycle_log.csv shows {tier_in_log}"

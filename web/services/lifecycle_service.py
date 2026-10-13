from abc import ABC, abstractmethod
import os
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import pandas as pd

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_FILE = PROJECT_ROOT / "results" / "importance_scores.csv"
LOG_FILE = PROJECT_ROOT / "results" / "lifecycle_log.csv"
IMAGE_DIR = PROJECT_ROOT / "dataset" / "processed"
CLOUD_DIR = PROJECT_ROOT / "cloud_simulation"

STORAGE_DIRS = {
    "S3_STANDARD": CLOUD_DIR / "S3_STANDARD",
    "S3_STANDARD_IA": CLOUD_DIR / "S3_STANDARD_IA",
    "S3_GLACIER": CLOUD_DIR / "S3_GLACIER",
}

# The only accepted tier names; any other value is rejected.
SUPPORTED_TIERS = frozenset(STORAGE_DIRS.keys())


class BaseStorageService(ABC):
    """Abstract interface for satellite cloud storage lifecycle management."""

    @abstractmethod
    def store_and_apply_lifecycle(
        self,
        image_name: str,
        source_path: Path,
        score: float,
        category: str,
        storage_class: str
    ) -> Dict[str, Any]:
        """Store image and record lifecycle transition."""
        pass

    @abstractmethod
    def get_lifecycle_log(self) -> List[Dict[str, Any]]:
        """Retrieve recent lifecycle records."""
        pass


class LocalSimulationStorageService(BaseStorageService):
    """
    Local simulation storage service that manages local tier folders
    (S3_STANDARD, S3_STANDARD_IA, S3_GLACIER) and records actions to lifecycle_log.csv.
    """

    def __init__(self):
        # Ensure directories exist
        for path in STORAGE_DIRS.values():
            path.mkdir(parents=True, exist_ok=True)
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    def get_lifecycle_log(self) -> List[Dict[str, Any]]:
        """
        Read results/lifecycle_log.csv dynamically.
        Gracefully handles missing or empty log files.
        """
        if not LOG_FILE.exists():
            return []

        try:
            df = pd.read_csv(LOG_FILE)
            records = df.to_dict(orient="records")
            # Format numbers consistently
            for item in records:
                try:
                    item["importance_score"] = float(item["importance_score"])
                except (ValueError, TypeError):
                    pass
            return records
        except Exception as e:
            print(f"Error reading lifecycle log: {e}")
            return []

    def store_and_apply_lifecycle(
        self,
        image_name: str,
        source_path: Path,
        score: float,
        category: str,
        storage_class: str
    ) -> Dict[str, Any]:
        """
        Place image in the designated simulated storage tier directory
        and append record to results/lifecycle_log.csv and results/importance_scores.csv.

        Returns a dict with key ``error`` (and HTTP-compatible ``status_code``) when
        the operation cannot be completed; callers must check for this key.
        """
        # --- 1. Validate storage class ----------------------------------------
        if storage_class not in SUPPORTED_TIERS:
            return {
                "error": (
                    f"Invalid storage class '{storage_class}'. "
                    f"Supported tiers are: {', '.join(sorted(SUPPORTED_TIERS))}."
                ),
                "status_code": 400,
                "image_name": image_name,
            }

        # --- 2. Require source image to exist ---------------------------------
        source_path = Path(source_path)
        if not source_path.exists():
            return {
                "error": (
                    f"Source image '{source_path.name}' does not exist at "
                    f"'{source_path}'. Cannot record a copy that was never made."
                ),
                "status_code": 404,
                "image_name": image_name,
            }

        # --- 3. Copy to the target tier ---------------------------------------
        target_dir = STORAGE_DIRS[storage_class]
        target_dir.mkdir(parents=True, exist_ok=True)
        dest_path = target_dir / image_name
        shutil.copy2(source_path, dest_path)
        action = f"Copied to {storage_class}"

        # --- 4. Remove stale copies from other tiers -------------------------
        for tier, tier_path in STORAGE_DIRS.items():
            if tier == storage_class:
                continue
            stale = tier_path / image_name
            if stale.exists():
                stale.unlink()

        # --- 5. Build the canonical record ------------------------------------
        new_record = {
            "image_name": image_name,
            "importance_score": round(score, 2),
            "category": category,
            "storage_class": storage_class,
            "action": action,
        }

        # --- 6. Update lifecycle_log.csv (one row per image_name) ------------
        records = self.get_lifecycle_log()
        records = [r for r in records if r.get("image_name") != image_name]
        records.append(new_record)
        pd.DataFrame(records).to_csv(LOG_FILE, index=False)

        # --- 7. Update importance_scores.csv (one row per image_name) --------
        self._update_importance_scores(image_name, score, category, storage_class)

        return new_record

    def _update_importance_scores(
        self,
        image_name: str,
        score: float,
        category: str,
        storage_class: str
    ) -> None:
        """Update or append entry in results/importance_scores.csv."""
        if not RESULTS_FILE.exists():
            df = pd.DataFrame(columns=["image_name", "importance_score", "category", "storage_class"])
        else:
            df = pd.read_csv(RESULTS_FILE)

        # Remove existing if present to update
        df = df[df["image_name"] != image_name]
        new_row = pd.DataFrame([{
            "image_name": image_name,
            "importance_score": round(score, 2),
            "category": category,
            "storage_class": storage_class
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(RESULTS_FILE, index=False)

    def get_storage_inventory(self) -> Dict[str, Any]:
        """Inspect the local simulated storage buckets."""
        inventory = {}
        total_files = 0
        total_size = 0

        for tier, path in STORAGE_DIRS.items():
            files = []
            if path.exists():
                for f in path.glob("*.*"):
                    sz = f.stat().st_size
                    files.append({
                        "filename": f.name,
                        "size_bytes": sz,
                        "size_kb": round(sz / 1024, 2),
                        "modified": f.stat().st_mtime
                    })
                    total_size += sz
            inventory[tier] = {
                "count": len(files),
                "files": files
            }
            total_files += len(files)

        return {
            "tiers": inventory,
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2)
        }


class S3StorageService(BaseStorageService):
    """
    AWS S3 Storage Service placeholder.
    Architecture abstraction for future live AWS cloud deployment.
    """

    def __init__(
        self,
        region: Optional[str] = None,
        bucket: Optional[str] = None,
        dynamodb_table: Optional[str] = None
    ):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.bucket = bucket or os.getenv("S3_BUCKET", "satellite-archive-storage-2026")
        self.table = dynamodb_table or os.getenv("DYNAMODB_TABLE", "SatelliteLifecycleMetadata")

    def store_and_apply_lifecycle(
        self,
        image_name: str,
        source_path: Path,
        score: float,
        category: str,
        storage_class: str
    ) -> Dict[str, Any]:
        raise NotImplementedError(
            f"S3StorageService is configured for AWS S3 Bucket: '{self.bucket}' in '{self.region}'. "
            "Please use LocalSimulationStorageService for local prototype execution."
        )

    def get_lifecycle_log(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("S3StorageService lifecycle log is managed in AWS CloudWatch / DynamoDB.")


# Global singleton instance for local simulation
lifecycle_service = LocalSimulationStorageService()

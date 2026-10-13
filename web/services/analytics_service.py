from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_FILE = PROJECT_ROOT / "results" / "importance_scores.csv"
LOG_FILE = PROJECT_ROOT / "results" / "lifecycle_log.csv"
PROCESSED_DIR = PROJECT_ROOT / "dataset" / "processed"
SAMPLE_DIR = PROJECT_ROOT / "dataset" / "sample"
CLOUD_DIR = PROJECT_ROOT / "cloud_simulation"

# Mirror of lifecycle_service.STORAGE_DIRS to avoid a circular import.
_STORAGE_DIRS = {
    "S3_STANDARD": CLOUD_DIR / "S3_STANDARD",
    "S3_STANDARD_IA": CLOUD_DIR / "S3_STANDARD_IA",
    "S3_GLACIER": CLOUD_DIR / "S3_GLACIER",
}


class AnalyticsService:
    """
    Analytics and Reporting Service for IntelliArchive.
    Reads dynamic CSV results and system paths without hardcoding values.
    """

    @staticmethod
    def load_scores_dataframe() -> pd.DataFrame:
        """Safely load results/importance_scores.csv into DataFrame."""
        if not RESULTS_FILE.exists():
            return pd.DataFrame(columns=["image_name", "importance_score", "category", "storage_class"])

        try:
            df = pd.read_csv(RESULTS_FILE)
            if "importance_score" in df.columns:
                df["importance_score"] = pd.to_numeric(df["importance_score"], errors="coerce").fillna(0.0)
            return df
        except Exception as e:
            print(f"Error loading scores CSV: {e}")
            return pd.DataFrame(columns=["image_name", "importance_score", "category", "storage_class"])

    @staticmethod
    def load_lifecycle_dataframe() -> pd.DataFrame:
        """Safely load results/lifecycle_log.csv into DataFrame."""
        if not LOG_FILE.exists():
            return pd.DataFrame(columns=["image_name", "importance_score", "category", "storage_class", "action"])

        try:
            df = pd.read_csv(LOG_FILE)
            if "importance_score" in df.columns:
                df["importance_score"] = pd.to_numeric(df["importance_score"], errors="coerce").fillna(0.0)
            return df
        except Exception as e:
            print(f"Error loading lifecycle CSV: {e}")
            return pd.DataFrame(columns=["image_name", "importance_score", "category", "storage_class", "action"])

    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Calculates dynamic KPIs for Dashboard and Analytics.
        No hard-coded values; all derived from actual result files.
        """
        df = self.load_scores_dataframe()

        total_images = len(df)

        category_counts = {
            "HIGH": int((df["category"] == "HIGH").sum()) if "category" in df.columns else 0,
            "MEDIUM": int((df["category"] == "MEDIUM").sum()) if "category" in df.columns else 0,
            "LOW": int((df["category"] == "LOW").sum()) if "category" in df.columns else 0,
        }

        storage_counts = {
            "S3_STANDARD": int((df["storage_class"] == "S3_STANDARD").sum()) if "storage_class" in df.columns else 0,
            "S3_STANDARD_IA": int((df["storage_class"] == "S3_STANDARD_IA").sum()) if "storage_class" in df.columns else 0,
            "S3_GLACIER": int((df["storage_class"] == "S3_GLACIER").sum()) if "storage_class" in df.columns else 0,
        }

        if total_images > 0 and "importance_score" in df.columns:
            scores = df["importance_score"]
            avg_score = round(float(scores.mean()), 2)
            max_score = round(float(scores.max()), 2)
            min_score = round(float(scores.min()), 2)
            median_score = round(float(scores.median()), 2)
            std_score = round(float(scores.std()) if total_images > 1 else 0.0, 2)

            max_row = df.loc[scores.idxmax()] if not df.empty else {}
            min_row = df.loc[scores.idxmin()] if not df.empty else {}
            highest_image = str(max_row.get("image_name", ""))
            lowest_image = str(min_row.get("image_name", ""))
        else:
            avg_score = 0.0
            max_score = 0.0
            min_score = 0.0
            median_score = 0.0
            std_score = 0.0
            highest_image = ""
            lowest_image = ""

        # Percentages
        category_pct = {
            k: round((v / total_images) * 100, 1) if total_images > 0 else 0.0
            for k, v in category_counts.items()
        }
        storage_pct = {
            k: round((v / total_images) * 100, 1) if total_images > 0 else 0.0
            for k, v in storage_counts.items()
        }

        return {
            "total_images": total_images,
            "categories": category_counts,
            "storage_classes": storage_counts,
            "category_percentages": category_pct,
            "storage_percentages": storage_pct,
            "avg_score": avg_score,
            "max_score": max_score,
            "min_score": min_score,
            "median_score": median_score,
            "std_score": std_score,
            "highest_image": highest_image,
            "lowest_image": lowest_image,
        }

    def get_chart_data(self) -> Dict[str, Any]:
        """Provides structured chart series for Chart.js."""
        df = self.load_scores_dataframe()

        if df.empty:
            return {
                "score_chart": {"labels": [], "data": [], "colors": []},
                "category_chart": {"labels": ["HIGH", "MEDIUM", "LOW"], "data": [0, 0, 0]},
                "storage_chart": {"labels": ["S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"], "data": [0, 0, 0]},
                "histogram_chart": {"labels": ["0-20", "21-40", "41-60", "61-80", "81-100"], "data": [0, 0, 0, 0, 0]}
            }

        # Clean shortened labels for cleaner chart rendering
        # e.g., "RGB-PanSharpen_AOI_2_Vegas_img1454_processed.jpg" -> "img1454"
        def simplify_label(name: str) -> str:
            parts = name.replace("_processed.jpg", "").replace(".jpg", "").split("_")
            for p in reversed(parts):
                if p.startswith("img") or len(p) <= 8:
                    return p
            return name[:12] + "..."

        labels = [simplify_label(name) for name in df["image_name"]]
        full_names = list(df["image_name"])
        scores = [round(float(s), 2) for s in df["importance_score"]]
        categories = list(df["category"])
        storages = list(df["storage_class"])

        category_counts = [
            int((df["category"] == "HIGH").sum()),
            int((df["category"] == "MEDIUM").sum()),
            int((df["category"] == "LOW").sum()),
        ]

        storage_counts = [
            int((df["storage_class"] == "S3_STANDARD").sum()),
            int((df["storage_class"] == "S3_STANDARD_IA").sum()),
            int((df["storage_class"] == "S3_GLACIER").sum()),
        ]

        # Histogram bins: [0, 20], [21, 40], [41, 60], [61, 80], [81, 100]
        bins = [0, 20, 40, 60, 80, 100]
        hist_counts, _ = np.histogram(scores, bins=bins)

        return {
            "score_chart": {
                "labels": labels,
                "full_names": full_names,
                "data": scores,
                "categories": categories,
                "storages": storages
            },
            "category_chart": {
                "labels": ["HIGH", "MEDIUM", "LOW"],
                "data": category_counts
            },
            "storage_chart": {
                "labels": ["S3_STANDARD", "S3_STANDARD_IA", "S3_GLACIER"],
                "data": storage_counts
            },
            "histogram_chart": {
                "labels": ["0–20", "21–40", "41–60", "61–80", "81–100"],
                "data": [int(x) for x in hist_counts]
            }
        }

    def get_archive_items(
        self,
        category: Optional[str] = None,
        storage_class: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns rich image archive records combining processed images,
        scores, and lifecycle logs.

        ``actual_storage_tier`` reflects the real on-disk location across all
        three simulation tier folders — not just the value stored in the CSV,
        which may lag after a tier transition.  ``exists_in_cloud`` is True
        only when the file is physically present in at least one tier folder.
        ``missing_from_cloud`` is True when the CSV says it should be archived
        but no tier folder contains the file.
        """
        df_scores = self.load_scores_dataframe()
        df_lifecycle = self.load_lifecycle_dataframe()

        # Build lookup from lifecycle log for recent actions
        action_map = {}
        if not df_lifecycle.empty:
            for _, r in df_lifecycle.iterrows():
                action_map[str(r.get("image_name"))] = str(r.get("action", "Stored"))

        items = []

        # Iterate over records in scores CSV
        for _, row in df_scores.iterrows():
            img_name = str(row["image_name"])
            cat = str(row["category"])
            s_class = str(row["storage_class"])  # CSV-stated tier (may be stale)
            score = float(row["importance_score"])

            # Filters
            if category and category.upper() != "ALL" and cat != category.upper():
                continue
            if storage_class and storage_class.upper() != "ALL" and s_class != storage_class.upper():
                continue
            if search and search.lower() not in img_name.lower():
                continue

            processed_path = PROCESSED_DIR / img_name

            # --- Ground-truth tier detection: scan all tier folders -----------
            actual_tier: Optional[str] = None
            actual_tier_path: Optional[Path] = None
            for tier, tier_dir in _STORAGE_DIRS.items():
                candidate = tier_dir / img_name
                if candidate.exists():
                    actual_tier = tier
                    actual_tier_path = candidate
                    break  # only one tier should hold the file after a valid store

            exists_in_cloud = actual_tier is not None
            # The file is "missing" when the CSV promises cloud storage but the
            # disk has no copy in any tier folder.
            missing_from_cloud = (not exists_in_cloud)

            # Use the ground-truth tier for display when available
            display_tier = actual_tier if actual_tier else s_class

            # File size: prefer the cloud copy, fall back to processed dir
            file_size_kb = 0.0
            if actual_tier_path and actual_tier_path.exists():
                file_size_kb = round(actual_tier_path.stat().st_size / 1024, 1)
            elif processed_path.exists():
                file_size_kb = round(processed_path.stat().st_size / 1024, 1)

            # Corresponding raw sample TIFF
            base_stem = img_name.replace("_processed.jpg", "")
            sample_tiff_name = f"{base_stem}.tif"
            sample_exists = (SAMPLE_DIR / sample_tiff_name).exists()

            # Reliable contrast-stretched preview (matching Analyze Image page visualization)
            thumbnail_url = f"/api/thumbnail/{img_name}"

            items.append({
                "image_name": img_name,
                "importance_score": score,
                "category": cat,
                "storage_class": display_tier,
                "actual_storage_tier": actual_tier,   # None when missing from cloud
                "action": action_map.get(img_name, f"Copied to {display_tier}"),
                "file_size_kb": file_size_kb,
                "processed_url": f"/images/processed/{img_name}",
                "thumbnail_url": thumbnail_url,
                "preview_url": thumbnail_url,
                "sample_tiff": sample_tiff_name if sample_exists else None,
                "exists_in_cloud": exists_in_cloud,
                "missing_from_cloud": missing_from_cloud,
                "lifecycle_status": "Active Archive" if exists_in_cloud else "Preprocessed",
            })

        return items

    def get_image_details(self, filename: str) -> Optional[Dict[str, Any]]:
        """Fetch complete detailed metadata for a single image."""
        items = self.get_archive_items()
        for item in items:
            if item["image_name"] == filename:
                return item
        return None

    def calculate_cost_savings(self) -> Dict[str, Any]:
        """
        Calculates theoretical monthly cloud storage cost comparison.
        AWS Pricing Model baseline:
        - S3 Standard: $0.023 / GB / month
        - S3 Standard-IA: $0.0125 / GB / month (~45% savings)
        - S3 Glacier: $0.0040 / GB / month (~82% savings)
        """
        metrics = self.get_summary_metrics()
        total_images = metrics["total_images"]
        if total_images == 0:
            return {
                "baseline_cost_per_tb": 23.00,
                "optimized_cost_per_tb": 23.00,
                "savings_pct": 0.0,
                "monthly_savings_per_tb": 0.0
            }

        counts = metrics["storage_classes"]
        p_std = counts["S3_STANDARD"] / total_images
        p_ia = counts["S3_STANDARD_IA"] / total_images
        p_glacier = counts["S3_GLACIER"] / total_images

        # Baseline: 100% S3 Standard ($23.00 per TB/month)
        baseline_cost_per_tb = 23.00

        # Optimized blended rate:
        optimized_cost_per_tb = (
            p_std * 23.00
            + p_ia * 12.50
            + p_glacier * 4.00
        )

        savings_per_tb = max(0.0, baseline_cost_per_tb - optimized_cost_per_tb)
        savings_pct = round((savings_per_tb / baseline_cost_per_tb) * 100, 1)

        return {
            "baseline_cost_per_tb": round(baseline_cost_per_tb, 2),
            "optimized_cost_per_tb": round(optimized_cost_per_tb, 2),
            "monthly_savings_per_tb": round(savings_per_tb, 2),
            "savings_pct": savings_pct,
            "tier_rates": {
                "S3_STANDARD": "$0.023 / GB ($23.00 / TB)",
                "S3_STANDARD_IA": "$0.0125 / GB ($12.50 / TB)",
                "S3_GLACIER": "$0.004 / GB ($4.00 / TB)"
            }
        }


# Global singleton instance
analytics_service = AnalyticsService()

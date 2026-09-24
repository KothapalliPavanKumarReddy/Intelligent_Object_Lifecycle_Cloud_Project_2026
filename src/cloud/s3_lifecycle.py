from pathlib import Path
import shutil
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_FILE = PROJECT_ROOT / "results" / "importance_scores.csv"
IMAGE_DIR = PROJECT_ROOT / "dataset" / "processed"
CLOUD_DIR = PROJECT_ROOT / "cloud_simulation"
LOG_FILE = PROJECT_ROOT / "results" / "lifecycle_log.csv"

STORAGE_DIRS = {
    "S3_STANDARD": CLOUD_DIR / "S3_STANDARD",
    "S3_STANDARD_IA": CLOUD_DIR / "S3_STANDARD_IA",
    "S3_GLACIER": CLOUD_DIR / "S3_GLACIER",
}


def simulate_lifecycle():

    df = pd.read_csv(RESULTS_FILE)

    lifecycle_records = []

    print("=" * 60)
    print("INTELLIGENT OBJECT LIFECYCLE SIMULATION")
    print("=" * 60)

    for _, row in df.iterrows():

        image_name = row["image_name"]
        score = row["importance_score"]
        category = row["category"]
        storage_class = row["storage_class"]

        source_path = IMAGE_DIR / image_name
        destination_dir = STORAGE_DIRS[storage_class]
        destination_path = destination_dir / image_name

        destination_dir.mkdir(parents=True, exist_ok=True)

        if source_path.exists():
            shutil.copy2(source_path, destination_path)
            action = "Copied to simulated storage"
        else:
            action = "Source image not found"

        lifecycle_records.append({
            "image_name": image_name,
            "importance_score": score,
            "category": category,
            "storage_class": storage_class,
            "action": action
        })

        print()
        print(f"Image          : {image_name}")
        print(f"Importance     : {score}")
        print(f"Category       : {category}")
        print(f"Storage Class  : {storage_class}")
        print(f"Action         : {action}")

    log_df = pd.DataFrame(lifecycle_records)
    log_df.to_csv(LOG_FILE, index=False)

    print()
    print("=" * 60)
    print("Lifecycle simulation complete.")
    print(f"Lifecycle log saved to:")
    print(LOG_FILE)
    print("=" * 60)


if __name__ == "__main__":
    simulate_lifecycle()

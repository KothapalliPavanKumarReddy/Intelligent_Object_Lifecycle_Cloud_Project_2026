from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Results file
RESULTS_FILE = PROJECT_ROOT / "results" / "importance_scores.csv"

# Output folder
OUTPUT_DIR = PROJECT_ROOT / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_dashboard():

    # Load results
    df = pd.read_csv(RESULTS_FILE)

    # Calculate distributions
    category_counts = df["category"].value_counts()
    storage_counts = df["storage_class"].value_counts()

    # ============================================================
    # 1. Importance Score Chart
    # ============================================================

    plt.figure(figsize=(12, 6))

    plt.bar(
        df["image_name"],
        df["importance_score"]
    )

    plt.xlabel("Satellite Images")
    plt.ylabel("Semantic Importance Score")
    plt.title("Satellite Image Importance Scores")

    plt.xticks(rotation=90, fontsize=7)
    plt.tight_layout()

    score_chart = OUTPUT_DIR / "importance_scores_chart.png"
    plt.savefig(score_chart, dpi=200)
    plt.close()

    # ============================================================
    # 2. Category Distribution Chart
    # ============================================================

    plt.figure(figsize=(8, 5))

    plt.bar(
        category_counts.index,
        category_counts.values
    )

    plt.xlabel("Importance Category")
    plt.ylabel("Number of Images")
    plt.title("Importance Category Distribution")

    plt.tight_layout()

    category_chart = OUTPUT_DIR / "category_distribution.png"
    plt.savefig(category_chart, dpi=200)
    plt.close()

    # ============================================================
    # 3. Storage Tier Distribution Chart
    # ============================================================

    plt.figure(figsize=(9, 5))

    plt.bar(
        storage_counts.index,
        storage_counts.values
    )

    plt.xlabel("Simulated Storage Tier")
    plt.ylabel("Number of Images")
    plt.title("Simulated Cloud Storage Distribution")

    plt.xticks(rotation=20)
    plt.tight_layout()

    storage_chart = OUTPUT_DIR / "storage_distribution.png"
    plt.savefig(storage_chart, dpi=200)
    plt.close()

    # ============================================================
    # Console Summary
    # ============================================================

    print("=" * 60)
    print("PROJECT RESULTS DASHBOARD")
    print("=" * 60)

    print()
    print("Total Images Processed:")
    print(len(df))

    print()
    print("Category Distribution:")
    print(category_counts)

    print()
    print("Storage Distribution:")
    print(storage_counts)

    print()
    print("Charts generated:")

    print(f"1. {score_chart}")
    print(f"2. {category_chart}")
    print(f"3. {storage_chart}")

    print()
    print("=" * 60)
    print("Dashboard generation complete.")
    print("=" * 60)


if __name__ == "__main__":
    create_dashboard()
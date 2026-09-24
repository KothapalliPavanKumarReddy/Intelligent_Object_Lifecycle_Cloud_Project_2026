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

    # Category counts
    category_counts = df["category"].value_counts()

    # Storage counts
    storage_counts = df["storage_class"].value_counts()

    # Create figure
    plt.figure(figsize=(10, 6))

    # Importance scores
    plt.bar(
        df["image_name"],
        df["importance_score"]
    )

    plt.xlabel("Satellite Images")
    plt.ylabel("Importance Score")
    plt.title("Satellite Image Importance Scores")

    plt.xticks(rotation=90, fontsize=7)

    plt.tight_layout()

    # Save chart
    output_file = OUTPUT_DIR / "importance_scores_chart.png"
    plt.savefig(output_file, dpi=200)

    plt.close()

    print("=" * 60)
    print("PROJECT RESULTS DASHBOARD")
    print("=" * 60)

    print()
    print("Category Distribution:")
    print(category_counts)

    print()
    print("Storage Distribution:")
    print(storage_counts)

    print()
    print(f"Dashboard chart saved to:")
    print(output_file)

    print()
    print("=" * 60)


if __name__ == "__main__":
    create_dashboard()
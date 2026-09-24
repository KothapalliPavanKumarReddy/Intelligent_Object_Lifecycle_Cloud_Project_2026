from pathlib import Path
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Processed satellite images
IMAGE_DIR = PROJECT_ROOT / "dataset" / "processed"

# Output file
OUTPUT_FILE = PROJECT_ROOT / "results" / "importance_scores.csv"

# Create results directory
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


# Load CLIP model
print("Loading CLIP Vision Foundation Model...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

model.eval()


# Text descriptions used to estimate image relevance
TEXT_PROMPTS = [
    "important satellite image containing urban infrastructure",
    "moderately important satellite image",
    "unimportant satellite image with little useful information"
]


def calculate_importance(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        text=TEXT_PROMPTS,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = outputs.logits_per_image.softmax(dim=1)[0]

    # Convert probabilities into a simple importance score
    score = (
        probabilities[0].item() * 100
        + probabilities[1].item() * 50
        + probabilities[2].item() * 0
    )

    return score


def classify_storage(score):

    if score >= 70:
        return "HIGH", "S3_STANDARD"

    elif score >= 40:
        return "MEDIUM", "S3_STANDARD_IA"

    else:
        return "LOW", "S3_GLACIER"


def main():

    image_files = list(IMAGE_DIR.glob("*.jpg"))

    if not image_files:
        print("No processed images found.")
        return

    print(f"Images found: {len(image_files)}")
    print()

    results = []

    for image_path in image_files:

        try:

            score = calculate_importance(image_path)

            category, storage_class = classify_storage(score)

            print(
                f"{image_path.name} "
                f"→ Score: {score:.2f} "
                f"→ {category} "
                f"→ {storage_class}"
            )

            results.append(
                f"{image_path.name},{score:.2f},{category},{storage_class}"
            )

        except Exception as error:

            print(
                f"Error processing {image_path.name}: {error}"
            )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(
            "image_name,importance_score,category,storage_class\n"
        )

        for row in results:
            file.write(row + "\n")

    print()
    print("Importance scoring complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

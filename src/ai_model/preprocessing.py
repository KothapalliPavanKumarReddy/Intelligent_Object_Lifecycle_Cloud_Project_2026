from pathlib import Path
from PIL import Image

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset folders
INPUT_DIR = PROJECT_ROOT / "dataset" / "sample"
OUTPUT_DIR = PROJECT_ROOT / "dataset" / "processed"

# Create output folder
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Target image size for the vision model
IMAGE_SIZE = (224, 224)


def preprocess_images():

    image_files = list(INPUT_DIR.glob("*.tif"))

    if not image_files:
        print("No TIFF images found in dataset/sample/")
        return

    processed_count = 0

    for image_path in image_files:

        try:
            print(f"Processing: {image_path.name}")

            # Open satellite image
            image = Image.open(image_path).convert("RGB")

            # Resize for vision model
            image = image.resize(IMAGE_SIZE)

            # Output filename
            output_name = f"{image_path.stem}_processed.jpg"
            output_path = OUTPUT_DIR / output_name

            # Save processed image
            image.save(output_path, "JPEG", quality=95)

            processed_count += 1

        except Exception as e:
            print(f"Skipped {image_path.name}: {e}")

    print()
    print("Processing complete!")
    print(f"Images processed: {processed_count}")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    preprocess_images()

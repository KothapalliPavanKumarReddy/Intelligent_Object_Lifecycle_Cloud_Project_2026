from pathlib import Path
import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = PROJECT_ROOT / "dataset" / "sample"
OUTPUT_DIR = PROJECT_ROOT / "dataset" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = (224, 224)


def enhance_image(image):
    """Stretch the image's actual pixel range to 0-255 for visualization."""
    array = np.asarray(image).astype(np.float32)

    enhanced = np.zeros_like(array)

    for channel in range(3):
        channel_data = array[:, :, channel]
        min_value = channel_data.min()
        max_value = channel_data.max()

        if max_value > min_value:
            enhanced[:, :, channel] = (
                (channel_data - min_value)
                / (max_value - min_value)
                * 255
            )
        else:
            enhanced[:, :, channel] = channel_data

    return Image.fromarray(enhanced.astype(np.uint8), "RGB")


def preprocess_images():
    image_files = list(INPUT_DIR.glob("*.tif"))

    if not image_files:
        print("No TIFF images found in dataset/sample/")
        return

    processed_count = 0

    for image_path in image_files:
        try:
            print(f"Processing: {image_path.name}")

            image = Image.open(image_path).convert("RGB")

            # Contrast stretch for the low-range satellite pixel values
            image = enhance_image(image)

            # Resize for CLIP
            image = image.resize(IMAGE_SIZE)

            output_name = f"{image_path.stem}_processed.jpg"
            output_path = OUTPUT_DIR / output_name

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
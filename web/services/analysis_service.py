from abc import ABC, abstractmethod
import io
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import numpy as np
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_SIZE = (224, 224)

# Semantic prompts used by the research prototype
TEXT_PROMPTS = [
    "important satellite image containing urban infrastructure",
    "moderately important satellite image",
    "unimportant satellite image with little useful information"
]


def enhance_satellite_image(image: Image.Image) -> Image.Image:
    """
    Stretch the image's actual pixel range to 0-255.
    Preserves and enhances satellite TIFF imagery with narrow dynamic ranges.
    Matches src/ai_model/preprocessing.py logic.
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

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
                * 255.0
            )
        else:
            enhanced[:, :, channel] = channel_data

    return Image.fromarray(np.clip(enhanced, 0, 255).astype(np.uint8), "RGB")


def classify_importance_and_storage(score: float) -> Tuple[str, str]:
    """
    Classify semantic score into lifecycle tier and storage class.
    Matches src/ai_model/importance_scoring.py logic:
    HIGH   -> S3_STANDARD     (Score >= 70)
    MEDIUM -> S3_STANDARD_IA  (Score >= 40)
    LOW    -> S3_GLACIER      (Score < 40)
    """
    if score >= 70.0:
        return "HIGH", "S3_STANDARD"
    elif score >= 40.0:
        return "MEDIUM", "S3_STANDARD_IA"
    else:
        return "LOW", "S3_GLACIER"


class BaseVisionService(ABC):
    """Abstract interface for satellite vision foundation models."""

    @abstractmethod
    def analyze_image(
        self,
        image_input: Union[Path, str, bytes, Image.Image]
    ) -> Dict[str, Any]:
        """Analyze satellite image and return importance metrics."""
        pass


class LocalCLIPService(BaseVisionService):
    """
    Local Vision Foundation Model Service using OpenAI CLIP ViT-B/32.
    Implements singleton model caching to avoid reloading weights across requests.
    """
    _instance: Optional["LocalCLIPService"] = None
    _model: Optional[CLIPModel] = None
    _processor: Optional[CLIPProcessor] = None
    _model_name: str = "openai/clip-vit-base-patch32"

    def __new__(cls) -> "LocalCLIPService":
        if cls._instance is None:
            cls._instance = super(LocalCLIPService, cls).__new__(cls)
        return cls._instance

    @property
    def is_loaded(self) -> bool:
        return self._model is not None and self._processor is not None

    def load_model(self) -> None:
        """Load and cache the CLIP model and processor in memory."""
        if not self.is_loaded:
            print(f"Loading cached CLIP Foundation Model ({self._model_name})...")
            self._model = CLIPModel.from_pretrained(self._model_name)
            self._processor = CLIPProcessor.from_pretrained(self._model_name)
            self._model.eval()
            print("CLIP Foundation Model ready for inference.")

    def preprocess_image(
        self,
        image_input: Union[Path, str, bytes, Image.Image],
        save_path: Optional[Path] = None
    ) -> Image.Image:
        """
        Ingest TIFF, PNG, or JPEG, apply satellite contrast stretching,
        and resize to 224x224.
        """
        if isinstance(image_input, Image.Image):
            pil_image = image_input
        elif isinstance(image_input, (str, Path)):
            pil_image = Image.open(image_input)
        elif isinstance(image_input, bytes):
            pil_image = Image.open(io.BytesIO(image_input))
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Contrast stretch for low-range satellite pixel values
        enhanced = enhance_satellite_image(pil_image)

        # Resize to model input size (224x224)
        processed = enhanced.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)

        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            processed.save(save_path, "JPEG", quality=95)

        return processed

    def analyze_image(
        self,
        image_input: Union[Path, str, bytes, Image.Image],
        filename: str = "uploaded_satellite_image.jpg",
        save_processed_to: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Run inference using the cached CLIP model.
        Returns importance score, tier category, storage recommendation,
        and prompt probabilities.
        """
        self.load_model()
        assert self._model is not None and self._processor is not None

        # Preprocess satellite image
        processed_image = self.preprocess_image(image_input, save_path=save_processed_to)

        # Run CLIP zero-shot inference
        inputs = self._processor(
            text=TEXT_PROMPTS,
            images=processed_image,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self._model(**inputs)

        probabilities = outputs.logits_per_image.softmax(dim=1)[0]
        prob_high = float(probabilities[0].item())
        prob_med = float(probabilities[1].item())
        prob_low = float(probabilities[2].item())

        # Exact formula from src/ai_model/importance_scoring.py
        score = prob_high * 100.0 + prob_med * 50.0 + prob_low * 0.0
        score = round(score, 2)

        category, storage_class = classify_importance_and_storage(score)

        return {
            "filename": filename,
            "importance_score": score,
            "category": category,
            "storage_class": storage_class,
            "probabilities": {
                "high_importance": round(prob_high * 100, 2),
                "medium_importance": round(prob_med * 100, 2),
                "low_importance": round(prob_low * 100, 2)
            },
            "model": self._model_name,
            "status": "Analysis Complete"
        }


class BedrockVisionService(BaseVisionService):
    """
    AWS Bedrock Vision Foundation Model placeholder.
    Architecture abstraction for future AWS cloud deployment.
    """
    def __init__(
        self,
        region: Optional[str] = None,
        model_id: Optional[str] = None
    ):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

    def analyze_image(
        self,
        image_input: Union[Path, str, bytes, Image.Image]
    ) -> Dict[str, Any]:
        raise NotImplementedError(
            f"BedrockVisionService is configured for AWS Cloud ({self.model_id} in {self.region}). "
            "Please use LocalCLIPService for local prototype execution."
        )


# Global singleton instance for local CLIP execution
clip_service = LocalCLIPService()

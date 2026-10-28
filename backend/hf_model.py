"""
This module handles Moondream2 inference via HuggingFace Transformers.
Runs locally on CPU — no GPU required.
"""

import io
import os

import torch
from PIL import Image
from transformers import AutoModelForCausalLM

TOKEN = os.environ.get("HF_TOKEN")


def init_model():
    model = AutoModelForCausalLM.from_pretrained(
        "vikhyatk/moondream2",
        trust_remote_code=True,
        dtype=torch.float16,
        token=TOKEN,
    )
    return model


def caption(model, image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    result = model.caption(image)
    return result["caption"]


def generate_name(model, image_bytes: bytes) -> str:
    """
    Derive a human-readable filename from the image-caption
    """
    prompt = (
        "Generate a short, memorable filename for this photo that captures its specific subject, action and/or scene. "
        "Prefer proper, names over generic categories."
        "Think about what concrete visual details make this photo memorable and lead with that."
        "Use only lowercase letters, numbers, and hyphens. Under 50 characters. Return only the filename, no extension, nothing else."
    )
    image = Image.open(io.BytesIO(image_bytes))
    result = model.query(image, prompt)
    name = result["answer"].strip().strip('"').strip()
    return name


def extract_name(img_caption: str) -> str:
    """
    Extract a photo's new name from the generated caption
    """
    # articles & prepositions to skip
    skip = {"a", "an", "the", "is", "are", "was", "in", "on", "at", "of", "and", "to", "for", "with"}
    words = img_caption.lower().split()
    # Take first 4-5 meaningful words
    meaningful = [w.strip(".,;:!?\"'()") for w in words if w.strip(".,;:!?\"'()").lower() not in skip]
    name = meaningful[:5]
    if not name:
        name = "photo"
    result = "-".join(name)
    return result[:50]

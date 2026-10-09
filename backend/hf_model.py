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


def generate_name(model, desc: str) -> str:
    """
    Derive a human-readable filename from the image-caption
    """
    prompt = (
        "Generate a short, memorable filename for this photo that captures its specific subject and scene. "
        "Prefer specific names over generic categories — a Ferrari is a 'ferrari', not a 'car'. "
        "Think about what detail makes this photo memorable and lead with that. "
        "Example: a classic Ferrari parked at a beach near a fruit stall should be 'ferrari-and-fruits-by-beach', not 'red-car-beach-backdrop'. "
        "Use only lowercase letters, numbers, and hyphens. Under 50 characters. Return only the filename, no extension, nothing else."
    )
    result = model.query(prompt, desc)
    name = result["answer"].strip().strip('"').strip()
    return name


def extract_name(caption: str) -> str:
    """
    Extract a photo's new name from the generated caption using text-only parsing
    """
    # articles & prepositions to skip
    skip = {"a", "an", "the", "is", "are", "was", "in", "on", "at", "of", "and", "to", "for", "with"}
    words = caption.lower().split()
    # Take first 4-5 meaningful words
    meaningful = [w.strip(".,;:!?\"'()") for w in words if w.strip(".,;:!?\"'()").lower() not in skip]
    name = meaningful[:5]
    if not name:
        name = "photo"
    result = "-".join(name)
    return result[:50]

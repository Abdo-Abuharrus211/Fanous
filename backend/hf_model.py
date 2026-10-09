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
    # prompt = (
    #     "Generate a short, descriptive, human-friendly filename for this photo. "
    #     "Use only lowercase letters, numbers, and hyphens. No spaces or special characters. "
    #     "Keep it under 80 characters and descriptive of the main subject of the photo. Return only the filename, nothing else."
    # )

    # articles & prepositions to skip
    skip = {"a", "an", "the", "is", "are", "was", "in", "on", "at", "of", "and", "to", "for", "with"}
    words = desc.lower().split()
    # Take first 4-5 meaningful words
    meaningful = [w.strip(".,;:!?\"'()") for w in words if w.strip(".,;:!?\"'()").lower() not in skip]
    name = meaningful[:5]
    # prompt model for name from desc - not using anymore but keep for ref
    # result = model.query(prompt, desc)
    # name = result["answer"].strip().strip('"').strip()
    if not name:
        name = "photo"
    result = "-".join(name)
    return result[:50]
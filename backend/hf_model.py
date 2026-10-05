"""
This module handles Moondream2 inference via HuggingFace Transformers.
Runs locally on CPU — no GPU required.
"""

import io

import torch
from PIL import Image
from transformers import AutoModelForCausalLM


def init_model():
    model = AutoModelForCausalLM.from_pretrained(
        "vikhyatk/moondream2",
        trust_remote_code=True,
        dtype=torch.float16,
    )
    return model


def caption(model, image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    result = model.caption(image)
    return result["caption"]


def generate_name(model, image_bytes: bytes) -> str:
    """
    Generate a human-readable filename based on a trained model (Moondream2 model).
    """
    image = Image.open(io.BytesIO(image_bytes))
    prompt = (
        "Generate a short, descriptive, human-friendly filename for this photo. "
        "Use only lowercase letters, numbers, and hyphens. No spaces or special characters. "
        "Keep it under 50 characters. Return only the filename, nothing else."
    )
    result = model.query(image, prompt)
    name = result["answer"].strip().strip('"').strip()
    if not name:
        name = "photo"
    name = name.lower().replace(" ", "-")
    return name

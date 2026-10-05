"""
This module handles the Moondream model and all generative captioning.
The model runs locally on K3s cluster without a GPU
"""

import io
import os
import moondream as md
from PIL import Image


def init_model():
    """
    Initialize the Moondream model.
    Uses local Photon inference if MOONDREAM_API_KEY is not set.
    Uses cloud API if MOONDREAM_API_KEY is set.
    """
    api_key = os.environ.get("MOONDREAM_API_KEY")
    if api_key:
        return md.vl(api_key=api_key)
    return md.photon("moondream2")


def caption(model, image_bytes: bytes) -> str:
    """
    Generate a descriptive caption for the image.
    """
    image = Image.open(io.BytesIO(image_bytes))
    result = model.caption(image, length="short")
    return result["caption"]


def generate_name(model, image_bytes: bytes) -> str:
    """
    Ask the model to generate a short, human-friendly filename for the image.
    """
    image = Image.open(io.BytesIO(image_bytes))
    prompt = (
        "Generate a short, descriptive, human-friendly filename for this photo. "
        "Use only lowercase letters, numbers, and hyphens. No spaces or special characters. "
        "Keep it under 50 characters. Return only the filename, nothing else."
    )
    result = model.query(image, prompt)
    # clean up result
    name = result["answer"].strip().strip('"').strip()
    if not name:
        name = "photo"
    name = name.lower().replace(" ", "-")
    return name

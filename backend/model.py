"""
This module handles the Moondream SDK and all generative captioning.
"""

import moondream as moondream
from PIL import Image

# init model
model = moondream.photon("moondream2")  # check if this is correct name


# TODO:
# Generate caption function
def caption(img) -> str:
    answer = model.caption(img)
    return answer

# Placeholder for generating a new name from the caption
def new_name_from_caption(caption: str) -> str:
    """
    Generate a new name for the image based on the caption.
    """
    new_name = f"new name {caption}"
    new_name = model.query("based on the caption you generated, pls generate a short and descriptive human-friendly and readable file name for this photo.")
    return new_name






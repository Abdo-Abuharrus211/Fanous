"""
This module handles Moondream2 inference via HuggingFace Transformers.
Runs locally on CPU — no GPU required.
"""

import io
import os

import torch
from PIL import Image
from transformers import AutoModelForCausalLM
from model import BaseModel

TOKEN = os.environ.get("HF_TOKEN")


class HuggingFaceTransformerModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.init_model()

    def init_model(self):
        model = AutoModelForCausalLM.from_pretrained(
            "vikhyatk/moondream2",
            trust_remote_code=True,
            dtype=torch.float16,
            token=TOKEN,
        )
        self.model = model

    def caption(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        result = self.model.caption(image)
        return result["caption"]

    def generate_name(self, image_bytes: bytes) -> str:
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
        result = self.model.query(image, prompt)
        name = result["answer"].strip().strip('"').strip()
        return name

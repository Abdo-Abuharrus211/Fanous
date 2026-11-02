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
            revision="2025-06-21",
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
        image = Image.open(io.BytesIO(image_bytes))
        result = self.model.query(image, self.name_gen_prompt)
        name = result["answer"].strip().strip('"').strip()
        return name

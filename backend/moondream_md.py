"""
This module handles the Moondream model and all generative captioning.
The model runs locally on K3s cluster without a GPU
"""

import io
import moondream as md
from PIL import Image
import model
from config import Settings


class MoondreamMD(model.BaseModel):

    def __init__(self):
        """
            Initialize the Moondream model using Photon.
            Uses local Photon inference if MOONDREAM_API_KEY is not set.
            Uses cloud API if MOONDREAM_API_KEY is set.
            """
        super().__init__()
        api_key = Settings.moondream_api_key
        if api_key:
            self.model = md.vl(api_key=api_key)
        else:
            self.model = md.photon("moondream2")

    def caption(self, image_bytes: bytes) -> str:
        """
        Generate a descriptive caption for the image.
        """
        result = self.model.caption(Image.open(io.BytesIO(image_bytes)))
        if not result:
            raise RuntimeError("Captioning process failed")
        return result["caption"]

    def generate_name(self, image_bytes: bytes) -> str:
        """
        Derive a human-readable filename from the image-caption
        """
        image = Image.open(io.BytesIO(image_bytes))
        result = self.model.query(image, self.name_gen_prompt)
        # clean up result
        if not result:
            raise RuntimeError("Name generation process failed")
        name = result["answer"].strip().strip('"').strip()
        return name

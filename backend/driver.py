"""
The Driver class manages a session's request state, instances of the VL model,
and facilitates processing business logic.
"""

import asyncio

from moondream_md import MoondreamMD as MD_Photon
from config import ModelMode
from hf_model import HuggingFaceTransformerModel as HF_Model


class Driver:
    def __init__(self, mode: ModelMode, session_id: str = "default"):
        self.session_id = session_id
        self._model_instance = None
        self.model_mode = mode
        self.state = {}

    @property
    def model(self):
        if self._model_instance is None:
            if self.model_mode is ModelMode.moondream_hf:
                self._model_instance = HF_Model()
            else:
                self._model_instance = MD_Photon()
        return self._model_instance

    async def process(self, image_bytes: bytes) -> dict:
        model = self.model
        description = await asyncio.to_thread(model.caption, image_bytes)
        name = await asyncio.to_thread(model.generate_name, image_bytes)
        return {"name": name, "description": description}


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

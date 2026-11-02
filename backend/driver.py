"""
The Driver class manages a session's request state, instances of the VL model,
and facilitates processing business logic.
"""
# TODO: In future, Will refactor in future to be modular via dependency injection or composition so less repetitive code

from moondream import init_model as init_vl_model, caption as vl_caption, generate_name as vl_generate_name
from model_modes import ModelMode
from hf_model import HuggingFaceTransformerModel as HF_Model


class Driver:
    def __init__(self, mode: ModelMode, session_id: str = "default"):
        self.session_id = session_id
        self._model = None
        self.model_mode = mode
        self.state = {}

    @property
    def get_model(self):
        if self._model is None:
            if self.model_mode is ModelMode.huggingface:
                self._model = HF_Model()
            else:
                self._model = init_vl_model()
        return self._model

    async def process(self, image_bytes: bytes) -> dict:
        model = self.get_model
        description = model.caption(image_bytes)
        name = model.generate_name(image_bytes)
        return {"name": name, "description": description}

    # async def process_with_hf(self, image_bytes: bytes) -> dict:
    #     model = self.get_model
    #     description = model.caption(image_bytes)
    #     name = model.generate_name(image_bytes)
    #     return {"name": name, "description": description}
    #
    # async def process(self, image_bytes: bytes) -> dict:
    #     model = self.get_model
    #     description = vl_caption(model, image_bytes)
    #     name = vl_generate_name(model, image_bytes)
    #     return {"name": name, "description": description}

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
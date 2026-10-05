"""
The Driver class manages a session's request state, instances of the VL model,
and facilitates processing business logic.
"""
# TODO: In future, Will refactor in future to be modular via dependency injection or composition so less repetitive code

from hf_model import init_model as init_hf_model, caption as hf_caption, generate_name as hf_generate_name
from model import init_model as init_vl_model, caption as vl_caption, generate_name as vl_generate_name
from model_modes import ModelMode


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
                self._model = init_hf_model()
            else:
                self._model = init_vl_model()
        return self._model

    async def process_with_hf(self, image_bytes: bytes) -> dict:
        model = self.get_model
        description = hf_caption(model, image_bytes)
        name = hf_generate_name(model, description)

        return {"name": name, "description": description}

    async def process(self, image_bytes: bytes) -> dict:
        model = self.get_model
        description = vl_caption(model, image_bytes)
        name = vl_generate_name(model, image_bytes)

        return {"name": name, "description": description}

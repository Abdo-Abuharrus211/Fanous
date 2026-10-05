"""
The Driver class manages a session's request state, instances of the VL model,
and facilitates processing business logic.
"""
# TODO: In future, Will refactor in future to be modular via dependency injection or composition so less repetitive code

from hf_model import init_model as init_hf_model, caption as hf_caption, generate_name as hf_generate_name
from model import init_model as init_vl_model, caption as vl_caption, generate_name as vl_generate_name


class Driver:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self._model = None
        self._tokenizer = None
        self._vl_model = None
        self.state = {}

    @property
    def model_pair(self):
        if self._model is None:
            self._model, self._tokenizer = init_hf_model()
        return self._model, self._tokenizer

    def vl_model(self):
        if self._vl_model is None:
            self._vl_model = init_vl_model()
        return self._vl_model

    async def process_with_tokenizer(self, image_bytes: bytes) -> dict:
        model, tokenizer = self.model_pair
        description = hf_caption(model, tokenizer, image_bytes)
        name = hf_generate_name(model, tokenizer, image_bytes)

        return {"name": name, "description": description}

    async def process(self, image_bytes: bytes) -> dict:
        model = self.vl_model()
        description = vl_caption(model, image_bytes)
        name = vl_generate_name(model, image_bytes)

        return {"name": name, "description": description}

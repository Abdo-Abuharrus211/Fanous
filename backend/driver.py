"""
The Driver class manages a session's request state, instances of the VL model,
and facilitates processing business logic.
"""

from model import init_model, caption, generate_name


class Driver:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self._vl_model = None
        self.state = {}

    @property
    def vl_model(self):
        if self._vl_model is None:
            self._vl_model = init_model()
        return self._vl_model

    async def process(self, image_bytes: bytes) -> dict:
        """
        Process the image payload, generate a caption and descriptive name.
        """
        description = caption(self.vl_model, image_bytes)
        name = generate_name(self.vl_model, image_bytes)

        return {"name": name, "description": description}

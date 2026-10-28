"""
The base Model class with methods to caption and generate names for images.
"""


class BaseModel:
    def __init__(self):
        self.model = None

    def caption(self, image_bytes: bytes) -> str:
        """
        Generate a descriptive caption for the image.
        """
        pass

    def generate_name(self, image_bytes: bytes) -> str:
        """
            Derive a human-readable filename from the image-caption
        """
        pass

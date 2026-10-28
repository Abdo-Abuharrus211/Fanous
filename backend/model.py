"""
The base Model class with methods to caption and generate names for images.
"""
import io
from PIL import Image


class Model:
    def __init__(self, model):
        self.model = model

    def caption(self, image_bytes: bytes) -> str:
        """
        Generate a descriptive caption for the image.
        """
        image = Image.open(io.BytesIO(image_bytes))
        result = self.model.caption(image)
        return result["caption"]

    def generate_name(self, model, image_bytes: bytes) -> str:
        """
            Derive a human-readable filename from the image-caption
        """
        image = Image.open(io.BytesIO(image_bytes))
        prompt = (
            "Generate a short, memorable filename for this photo that captures its specific subject, action and/or scene. "
            "Prefer proper, names over generic categories."
            "Think about what concrete visual details make this photo memorable and lead with that."
            "Use only lowercase letters, numbers, and hyphens. Under 50 characters. Return only the filename, no extension, nothing else."
        )
        result = self.model.query(image, prompt)
        name = result["answer"].strip().strip('"').strip()
        return name

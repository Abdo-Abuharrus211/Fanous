"""
The base Model class with methods to caption and generate names for images.
"""
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self):
        self.model = None
        self.name_gen_prompt = (
            "Generate a short, memorable filename for this photo that captures its specific subject, action and/or scene. "
            "Prefer proper names over generic categories."
            "Think about what concrete visual details make this photo memorable and lead with that."
            "Use only lowercase letters, numbers, and hyphens. Under 50 characters. Return only the filename, no extension, nothing else."
        )

    @abstractmethod
    def caption(self, image_bytes: bytes) -> str:
        """
        Generate a descriptive caption for the image.
        """
        pass

    @abstractmethod
    def generate_name(self, image_bytes: bytes) -> str:
        """
            Derive a human-readable filename from the image-caption
        """
        pass

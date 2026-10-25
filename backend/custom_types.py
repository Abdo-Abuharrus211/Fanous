from pydantic import BaseModel


class CaptionResponse(BaseModel):
    name: str
    description: str


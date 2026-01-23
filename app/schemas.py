from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=120)
    num_slides: int = Field(..., ge=1, le=30)

class SlideContent(BaseModel):
    title: str
    bullets: List[str]
    image_keyword: Optional[str] = ""

class GeminiOutline(BaseModel):
    presentation_title: str
    subtitle: str
    slides: List[SlideContent]
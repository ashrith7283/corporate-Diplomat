from pydantic import BaseModel
from typing import Optional

class TranslationTaskOutput(BaseModel):
    translated_text: str

class ReviewTaskOutput(BaseModel):
    final_text: str
    notes: Optional[str]

from pydantic import BaseModel
from typing import Optional

class TranslateRequest(BaseModel):
    text: str
    direction: str  # "casual_to_corporate" or "corporate_to_casual"

class TranslateResponse(BaseModel):
    translated: str
    notes: Optional[str]

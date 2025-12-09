# api/schemas/chat.py
from pydantic import BaseModel
from typing import List, Optional

class Source(BaseModel):
    file: str
    page: Optional[int] = None
    text: str = ""

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
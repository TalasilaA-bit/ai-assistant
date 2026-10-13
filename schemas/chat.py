# Pydantic schemas for request/response serialisation

from pydantic import BaseModel, Field
from typing import List

class ChatMessage(BaseModel):
    role: str = Field(..., description="Must be either 'human' or 'ai'")
    text: str = Field(..., description="The message textual content")

class ChatRequest(BaseModel):
    user_query: str
    chat_history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    answer: str

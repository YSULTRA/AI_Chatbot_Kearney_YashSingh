from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    """Response model with answer and sources"""
    answer: str
    sources: List[dict]
    relevant_context: List[str]

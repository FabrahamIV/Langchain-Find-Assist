from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- Request schemas ----------

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    message: str


# ---------- Response schemas ----------

class MessageResponse(BaseModel):
    message_id: str
    role: str
    content: str
    file_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationListItem(BaseModel):
    """Lightweight conversation object for sidebar listing."""
    conversation_id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    message_count: int = 0

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    """Full conversation with messages."""
    conversation_id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True


class FileResponse(BaseModel):
    file_id: str
    original_filename: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    pinecone_indexed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    user_id: str
    conversation_id: str
    reply: str
    state_keys: list[str] = []
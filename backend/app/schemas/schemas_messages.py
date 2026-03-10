from pydantic import BaseModel

class MessageCreate(BaseModel):
    chat_id: str
    role: str
    content: str
    file: str
    created_at: str
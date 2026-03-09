from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    user_id = Column(String, ForeignKey("users.id"))
    role = Column(String)
    message = Column(String)
    file = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")
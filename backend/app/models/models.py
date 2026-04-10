from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database_chat import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    files = relationship("UploadedFile", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"
    user_id = Column(String, ForeignKey("users.user_id"))
    conversation_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    files = relationship("UploadedFile", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    user_id = Column(String, ForeignKey("users.user_id"))
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String)  # "user" or "assistant"
    content = Column(String)
    file_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")
    files = relationship("UploadedFile", back_populates="message", cascade="all, delete-orphan")


class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    user_id = Column(String, ForeignKey("users.user_id"))
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))   
    message_id = Column(String, ForeignKey("messages.message_id"))
    file_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    pinecone_indexed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="files")
    conversation = relationship("Conversation", back_populates="files")
    message = relationship("Message", back_populates="files")

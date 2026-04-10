from sqlalchemy.orm import Session
from app.models.models import User, Conversation, Message, UploadedFile
from datetime import datetime


# ==================== User CRUD ====================

def get_or_create_user(db: Session, user_id: str | None = None) -> User:
    """Get existing user by ID, or create a new one."""
    if user_id:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            return user

    # Fallback: get the first user or create one
    user = db.query(User).first()
    if not user:
        user = User()
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# ==================== Conversation CRUD ====================

def create_conversation(db: Session, user_id: str, title: str = "New Chat") -> Conversation:
    conv = Conversation(user_id=user_id, title=title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def get_conversations(db: Session, user_id: str | None = None) -> list[Conversation]:
    """List all conversations, optionally filtered by user, newest first."""
    query = db.query(Conversation)
    if user_id:
        query = query.filter(Conversation.user_id == user_id)
    return query.order_by(Conversation.updated_at.desc()).all()


def get_conversation(db: Session, conversation_id: str) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()


def get_or_create_conversation(db: Session, conversation_id: str | None, user_id: str) -> Conversation:
    """Get an existing conversation or create a new one."""
    if conversation_id:
        conv = get_conversation(db, conversation_id)
        if conv:
            return conv
    return create_conversation(db, user_id)


def update_conversation_title(db: Session, conversation_id: str, title: str) -> Conversation | None:
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.title = title
        conv.updated_at = datetime.now()
        db.commit()
        db.refresh(conv)
    return conv


def delete_conversation(db: Session, conversation_id: str) -> bool:
    conv = get_conversation(db, conversation_id)
    if conv:
        db.delete(conv)
        db.commit()
        return True
    return False


# ==================== Message CRUD ====================

def create_message(
    db: Session,
    user_id: str,
    conversation_id: str,
    role: str,
    content: str,
    file_name: str | None = None,
    created_at: datetime | None = None,
) -> Message:
    msg = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
        file_name=file_name,
        created_at=created_at,
    )
    db.add(msg)
    # Also update conversation's updated_at timestamp
    conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if conv:
        conv.updated_at = datetime.now()
    db.commit()
    db.refresh(msg)
    return msg


def get_messages_by_conversation(db: Session, conversation_id: str) -> list[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )


# ==================== File CRUD ====================

def create_file_record(
    db: Session,
    user_id: str,
    conversation_id: str,
    original_filename: str,
    stored_path: str,
    message_id: str | None = None,
    file_id: str | None = None,
    file_size: int | None = None,
    mime_type: str | None = None,
    pinecone_indexed: bool = False,
    created_at: datetime | None = None,
) -> UploadedFile:
    record = UploadedFile(
        user_id=user_id,
        conversation_id=conversation_id,
        message_id=message_id,
        original_filename=original_filename,
        stored_path=stored_path,
        file_size=file_size,
        mime_type=mime_type,
        pinecone_indexed=pinecone_indexed,
        created_at=created_at,
    )
    if file_id:
        record.file_id = file_id
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_files_by_conversation(db: Session, conversation_id: str) -> list[UploadedFile]:
    return (
        db.query(UploadedFile)
        .filter(UploadedFile.conversation_id == conversation_id)
        .order_by(UploadedFile.created_at.asc())
        .all()
    )


def mark_file_indexed(db: Session, file_id: str) -> UploadedFile | None:
    record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if record:
        record.pinecone_indexed = True
        db.commit()
        db.refresh(record)
    return record

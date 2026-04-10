from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database_chat import get_db
from app.crud.crud import (
    get_or_create_user,
    get_conversations,
    get_conversation,
    create_conversation,
    update_conversation_title,
    delete_conversation,
    get_messages_by_conversation,
)
from app.schemas.schemas import ConversationListItem, ConversationDetail, MessageResponse

router = APIRouter()


@router.get("/conversations", response_model=list[ConversationListItem])
def list_conversations(user_id: str | None = None, db: Session = Depends(get_db)):
    """List all conversations for the sidebar."""
    convs = get_conversations(db, user_id)
    result = []
    for c in convs:
        result.append(ConversationListItem(
            conversation_id=c.conversation_id,
            title=c.title or "New Chat",
            created_at=c.created_at,
            updated_at=c.updated_at,
            message_count=len(c.messages),
        ))
    return result


@router.post("/conversations", response_model=ConversationDetail)
def new_conversation(user_id: str | None = None, db: Session = Depends(get_db)):
    """Create a new empty conversation."""
    user = get_or_create_user(db, user_id)
    conv = create_conversation(db, user.user_id)
    return ConversationDetail(
        conversation_id=conv.conversation_id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[],
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation_detail(conversation_id: str, db: Session = Depends(get_db)):
    """Get a conversation with all its messages (for loading chat history)."""
    conv = get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = get_messages_by_conversation(db, conversation_id)
    return ConversationDetail(
        conversation_id=conv.conversation_id,
        title=conv.title or "New Chat",
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[
            MessageResponse(
                message_id=m.message_id,
                role=m.role,
                content=m.content,
                file_name=m.file_name,
                created_at=m.created_at,
            )
            for m in messages
        ],
    )


@router.patch("/conversations/{conversation_id}")
def patch_conversation(conversation_id: str, title: str, db: Session = Depends(get_db)):
    """Update conversation title."""
    conv = update_conversation_title(db, conversation_id, title)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conv.conversation_id, "title": conv.title}


@router.delete("/conversations/{conversation_id}")
def remove_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Delete a conversation and all its messages/files (cascade)."""
    deleted = delete_conversation(db, conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": True}

import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from app.database.database_chat import get_db
from app.crud.crud import (
    get_or_create_user,
    get_or_create_conversation,
    update_conversation_title,
    create_message,
    create_file_record,
    mark_file_indexed,
)
from app.schemas.schemas import ChatResponse
from app.schemas.chat_schemas import ChatState
from app.agents.agents_chat_graph import app_graph

router = APIRouter()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "data/policies"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: Optional[str] = Form(None),
    conversation_id: Optional[str] = Form(None),
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """Main chat endpoint: handles message + optional file upload + RAG pipeline."""

    # 1. Get or create user
    user = get_or_create_user(db, user_id)

    # 2. Get or create conversation
    conversation = get_or_create_conversation(db, conversation_id, user.user_id)

    # 3. Handle file upload
    saved_path = None
    file_name = None
    if file:
        file_name = file.filename
        saved_path = UPLOAD_DIR / file_name

        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Record in DB
        file_record = create_file_record(
            db,
            conversation_id=conversation.conversation_id,
            user_id=user.user_id,
            original_filename=file_name,
            stored_path=str(saved_path),
            file_size=file.size if hasattr(file, "size") else None,
            mime_type=file.content_type,
        )

    # 4. Save user message to DB
    create_message(
        db,
        conversation_id=conversation.conversation_id,
        user_id=user.user_id,
        role="user",
        content=message,
        file_name=file_name,
    )

    # 5. Auto-title conversation from first user message
    if conversation.title == "New Chat":
        title = message[:40] if message.strip() else (file_name or "New Chat")
        update_conversation_title(db, conversation.conversation_id, title)

    # 6. Build state and invoke LangGraph RAG pipeline
    chat_state: ChatState = {
        "conversation_id": conversation.conversation_id,
        "message": message,
    }
    if saved_path:
        chat_state["file_path"] = str(saved_path)

    try:
        result = app_graph.invoke(chat_state)
        reply = result.get("answer", "Sorry, I could not generate a response.")

        # Mark file as indexed if we processed it
        if file and saved_path:
            mark_file_indexed(db, file_record.file_id)

    except Exception as e:
        print(f"RAG pipeline error: {e}")
        reply = f"Sorry, an error occurred while processing your request: {str(e)}"
        result = {}

    # 7. Save AI reply to DB
    create_message(
        db,
        conversation_id=conversation.conversation_id,
        user_id=user.user_id,
        role="assistant",
        content=reply,
    )

    return ChatResponse(
        user_id=user.user_id,
        conversation_id=conversation.conversation_id,
        reply=reply,
        state_keys=list(result.keys()) if result else [],
    )

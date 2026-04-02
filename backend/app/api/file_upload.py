from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from pathlib import Path
import shutil
from sqlalchemy.orm import Session

from app.database.database_chat import get_db
from app.models.models_messages import Message, User, Conversation
from app.agents.agents_state import ChatState
from app.agents.agents_chat_graph import app_graph

router = APIRouter()

UPLOAD_DIR = Path("data/policies")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # auto create folder

@router.post("/chat")
async def chat(
    message: str = Form(...),
    user_id: Optional[str] = Form(None),
    conversation_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    saved_path = None

    if file:
        saved_path = UPLOAD_DIR / file.filename

        # Save file to disk
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    print("Message:", message)
    if saved_path:
        print("Saved to:", saved_path)

    # Fetch or create User
    user = None
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = db.query(User).first()
        if not user:
            user = User()
            db.add(user)
            db.commit()
            db.refresh(user)

    # Fetch or create Conversation
    conversation = None
    if conversation_id:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        conversation = db.query(Conversation).first()
        if not conversation:
            conversation = Conversation(user_id=user.id, title="New Conversation")
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

    # Save user message to DB
    user_msg = Message(
        role="user",
        content=message,
        file=str(saved_path) if saved_path else None,
        user_id=user.id,
        conversation_id=conversation.id
    )
    db.add(user_msg)
    db.commit()

    # Build the initial state
    chat_state: ChatState = {
        "message": message,
        "conversation_id": conversation.id,
    }
    if saved_path:
        chat_state["file_path"] = str(saved_path)

    # Invoke the LangGraph application
    result = app_graph.invoke(chat_state)
    
    reply = result.get("answer", "Sorry, I could not generate a response.")

    # Save AI reply to DB
    ai_msg = Message(
        role="assistant",
        content=reply,
        user_id=user.id,
        conversation_id=conversation.id
    )
    db.add(ai_msg)
    db.commit()

    return {
        "reply": reply, 
        "state_keys": list(result.keys()),
        "user_id": user.id,
        "conversation_id": conversation.id
    }
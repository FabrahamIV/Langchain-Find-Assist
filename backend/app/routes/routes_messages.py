from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os

from database.database import get_db
from crud.message_crud import create_message, get_messages

router = APIRouter()

UPLOAD_DIR = "app/data/policies"

@router.post("/messages")
async def add_message(
    id: str = Form(...),
    role: str = Form(...),
    content: str = Form(...),
    file: UploadFile | None = File(None),
    created_at: str = Form(...),
    db: Session = Depends(get_db)
):

    return {
        "id": id,
        "role": role,
        "content": content,
        "file": file,
        "created_at": created_at
    }


@router.get("/messages")
def read_messages(db: Session = Depends(get_db)):
    return get_messages(db)
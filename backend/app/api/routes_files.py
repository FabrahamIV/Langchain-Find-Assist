from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from app.database.database_chat import get_db
from app.crud.crud import get_files_by_conversation
from app.schemas.schemas import FileResponse

router = APIRouter()


@router.get("/conversations/{conversation_id}/files", response_model=list[FileResponse])
def list_files(conversation_id: str, db: Session = Depends(get_db)):
    """List all files uploaded in a conversation."""
    files = get_files_by_conversation(db, conversation_id)
    return files


@router.get("/files/{file_id}/download")
def download_file(file_id: str, db: Session = Depends(get_db)):
    """Download/serve a stored file."""
    from app.models.models import UploadedFile

    record = db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = Path(record.stored_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FastAPIFileResponse(
        path=str(file_path),
        filename=record.original_filename,
        media_type=record.mime_type or "application/octet-stream",
    )

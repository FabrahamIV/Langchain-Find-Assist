from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pathlib import Path
import shutil

from app.services.services_file import load_docs
from app.agents.agents_state import ChatState

app = FastAPI()

UPLOAD_DIR = Path("data/policies")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # auto create folder

@app.post("/chat")
async def chat(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_text = ""
    saved_path = None
    all_docs = []

    if file:
        saved_path = UPLOAD_DIR / file.filename

        # Save file to disk
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the uploaded file
        state: ChatState = {"file_path": str(saved_path)}
        result = load_docs(state)
        all_docs = result.get("all_docs", [])
        
        # If you also want to read content:
        # contents = await file.read()
        # file_text = contents.decode("utf-8", errors="ignore")

    print("Message:", message)
    print("Saved to:", saved_path)
    print("Docs loaded:", len(all_docs))

    reply = f"You said: {message}. File processed: {file.filename if file else 'None'}"

    return {"reply": reply, "docs_count": len(all_docs)}
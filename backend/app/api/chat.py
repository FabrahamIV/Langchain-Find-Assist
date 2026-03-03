from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pathlib import Path
import shutil

app = FastAPI()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # auto create folder

@app.post("/chat")
async def chat(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_text = ""
    saved_path = None

    if file:
        saved_path = UPLOAD_DIR / file.filename

        # Save file to disk
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # If you also want to read content:
        contents = await file.read()
        file_text = contents.decode("utf-8", errors="ignore")

    print("Message:", message)
    print("Saved to:", saved_path)

    reply = f"You said: {message}"

    return {"reply": reply}
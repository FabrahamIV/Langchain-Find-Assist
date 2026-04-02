from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database_chat import get_db
from app.models.models_messages import User, Message
from app.api.file_upload import router as chat_router
from app.services.services_file import load_docs, create_chunks

app = FastAPI(title="Find-Assist API")

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend URL string
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat endpoints
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()

@app.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()

@app.get("/test-pipeline")
def test_pipeline():
    state: ChatState = {"file_path": "data/policies/"}
    state = load_docs(state)
    state = create_chunks(state)
    return state


if __name__ == "__main__":
    import uvicorn
    print("Starting Find-Assist API server...")
    uvicorn.run("app.main:app", host="[IP_ADDRESS]", port=8000, reload=True)

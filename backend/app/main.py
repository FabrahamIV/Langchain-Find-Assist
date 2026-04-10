import sys
import os

# Add the parent directory to sys.path so 'app' module is recognized when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Import Base and engine so create_all works after models are loaded
from app.database.database_chat import Base, engine

# Import all models so Base.metadata knows about them
from app.models.models import User, Conversation, Message, UploadedFile  # noqa: F401

# Import routers
from app.api.routes_chat import router as chat_router
from app.api.routes_conversations import router as conversations_router
from app.api.routes_files import router as files_router

app = FastAPI(title="Find-Assist API")

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(conversations_router, prefix="/api", tags=["conversations"])
app.include_router(files_router, prefix="/api", tags=["files"])


@app.on_event("startup")
def on_startup():
    """Create all database tables on startup (after models are imported)."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables ready.")


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    print("Starting Find-Assist API server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.agents.agents_debug_log import _agent_debug_log

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """FastAPI dependency that provides a DB session per request."""
    _agent_debug_log(
            hypothesis_id="H1",
            location="database_chat.get_db",
            message="Database connection established",
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

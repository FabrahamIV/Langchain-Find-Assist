from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

engine = create_engine("postgresql://fabraham:541789@127.0.0.1:5432/db_chat")
Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
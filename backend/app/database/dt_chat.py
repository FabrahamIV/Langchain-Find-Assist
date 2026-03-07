from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

engine = create_engine("sqlite:///chat.db")
Base = declarative_base()

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    file = Column(String)
    created_at = Column(DateTime, default=datetime.now())

Base.metadata.create_all(engine)
Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

session = Session()
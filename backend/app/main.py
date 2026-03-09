from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.db_models import User, Message

app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()

def main():
    print("Hello from find-assist!")


if __name__ == "__main__":
    main()

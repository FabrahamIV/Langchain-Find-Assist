from models.message import Message

def create_message(db, chat_id, role, content, file_path=None, created_at=None):
    msg = Message(
        chat_id=chat_id,
        role=role,
        content=content,
        file_path=file_path,
        created_at=created_at
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db):
    return db.query(Message).all()
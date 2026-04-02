from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import traceback
from app.models.models_messages import Message, User, Conversation

engine = create_engine("postgresql://fabraham:541789@127.0.0.1:5432/db_chat")
Session = sessionmaker(bind=engine)

def test_insert():
    try:
        with Session() as db:
            user = db.query(User).first()
            if not user:
                user = User()
                db.add(user)
                db.commit()
            
            conv = db.query(Conversation).first()
            if not conv:
                conv = Conversation(user_id=user.id, title="Test")
                db.add(conv)
                db.commit()
            
            msg = Message(
                role="user",
                content="test",
                file=None,
                user_id=user.id,
                conversation_id=conv.id
            )
            db.add(msg)
            db.commit()
            print("Successfully inserted message!")
    except Exception as e:
        with open("db_err2.txt", "w") as f:
            traceback.print_exc(file=f)

if __name__ == "__main__":
    test_insert()

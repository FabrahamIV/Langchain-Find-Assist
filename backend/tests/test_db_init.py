import sys
import os

# Add the project root (backend) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.database import engine, Base
from app.database.db_models import User, Conversation, Message

def test_db_init():
    print("Starting database initialization test...")
    try:
        # This will attempt to create tables if they don't exist
        # and check for relationship/mapping errors
        Base.metadata.create_all(bind=engine)
        print("Successfully created/verified database tables.")
        
        # Check if we can see the tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Current tables in database: {tables}")
        
        required_tables = ["users", "conversations", "messages"]
        for table in required_tables:
            if table in tables:
                print(f"  - Table '{table}' found.")
            else:
                print(f"  - Table '{table}' NOT found.")
                
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise e

if __name__ == "__main__":
    test_db_init()

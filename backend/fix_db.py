from sqlalchemy import create_engine, text

def fix_db():
    engine = create_engine("postgresql://fabraham:541789@127.0.0.1:5432/db_chat")
    
    columns_to_check = [
        "ALTER TABLE messages ADD COLUMN content VARCHAR;",
        "ALTER TABLE messages ADD COLUMN role VARCHAR;",
        "ALTER TABLE messages ADD COLUMN created_at TIMESTAMP;"
    ]
    
    for stmt in columns_to_check:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
            print(f"Success: {stmt}")
        except Exception as e:
            print(f"Skipped (likely already exists): {stmt} -> {str(e).splitlines()[0]}")

if __name__ == "__main__":
    fix_db()

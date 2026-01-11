import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

def setup_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salonp (
        thread_id INTEGER PRIMARY KEY,
        owner_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salonp_members (
        thread_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (thread_id, user_id)
    )
    """)

    conn.commit()

import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def setup_servers_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            server_id BIGINT PRIMARY KEY,
            review_channel_id BIGINT,
            embed_invitation_id BIGINT,
            spam_channel_id BIGINT,
            welcome_channel_id BIGINT,
            leave_channel_id BIGINT,
            boost_channel_id BIGINT,
            defense_active BOOLEAN DEFAULT FALSE,
            invitation_control_active BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_server(server_id: int) -> dict | None:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE server_id = %s", (server_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return None
    keys = [
        "server_id", "review_channel_id", "embed_invitation_id",
        "spam_channel_id", "welcome_channel_id", "leave_channel_id",
        "boost_channel_id", "defense_active", "invitation_control_active"
    ]
    return dict(zip(keys, row))

def ensure_server(server_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO servers (server_id) VALUES (%s) ON CONFLICT (server_id) DO NOTHING",
        (server_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def set_server_field(server_id: int, field: str, value):
    allowed = {
        "review_channel_id", "embed_invitation_id", "spam_channel_id",
        "welcome_channel_id", "leave_channel_id", "boost_channel_id",
        "defense_active", "invitation_control_active"
    }
    if field not in allowed:
        raise ValueError(f"Campo no permitido: {field}")
    ensure_server(server_id)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE servers SET {field} = %s WHERE server_id = %s",
        (value, server_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


def setup_servers_db():
    conn = get_conn()
    cursor = conn.cursor()

    # Crear tabla base si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            server_id BIGINT PRIMARY KEY,
            review_channel_id BIGINT,
            embed_invitation_id BIGINT,
            spam_channel_id BIGINT,
            welcome_channel_id BIGINT,
            leave_channel_id BIGINT,
            boost_channel_id BIGINT
        )
    """)

    # Migración automática: agregar columnas nuevas si no existen
    migrations = [
        "ALTER TABLE servers ADD COLUMN IF NOT EXISTS defense_active BOOLEAN DEFAULT FALSE",
        "ALTER TABLE servers ADD COLUMN IF NOT EXISTS invitation_control_active BOOLEAN DEFAULT FALSE",
    ]
    for sql in migrations:
        cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Base de datos de servidores lista")


def get_server(server_id: int) -> dict | None:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE server_id = %s", (server_id,))
    row = cursor.fetchone()

    if row:
        colnames = [desc[0] for desc in cursor.description]
        result = dict(zip(colnames, row))
    else:
        result = None

    cursor.close()
    conn.close()
    return result


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

import discord
from discord import app_commands
import os
import psycopg2

# ==========================
# CONFIGURACIÓN
# ==========================

# ID de la categoría donde se crearán los salones privados
CATEGORY_ID = 1460094093383307304

# Base de datos (Railway)
DATABASE_URL = "postgresql://postgres:mDxPNhPIKwMGpAtcZpMAgOZeZQmvDDLh@postgres.railway.internal:5432/railway"

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no está configurado en Railway")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

# ==========================
# CREACIÓN DE TABLAS (SIMPLE)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS salonp (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    owner_id BIGINT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS salonp_members (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL
)
""")

conn.commit()

# ==========================
# GRUPO DE COMANDOS
# ==========================

salonp_group = app_commands.Group(
    name="salonp",
    description="Comandos de salones privados"
)

# ==========================
# /salonp create
# ==========================

@salonp_group.command(
    name="create",
    description="Crea un salón privado"
)
async def salonp_create(interaction: discord.Interaction, nombre: str):
    guild = interaction.guild
    category = guild.get_channel(CATEGORY_ID)

    if not category:
        await interaction.response.send_message(
            "❌ Categoría no encontrada.",
            ephemeral=True
        )
        return

    # Verificar si ya tiene un salón
    cursor.execute(
        "SELECT channel_id FROM salonp WHERE owner_id=%s",
        (interaction.user.id,)
    )
    if cursor.fetchone():
        await interaction.response.send_message(
            "❌ Ya tienes un salón privado.",
            ephemeral=True
        )
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True
        )
    }

    channel = await guild.create_text_channel(
        name=nombre,
        category=category,
        overwrites=overwrites
    )

    # Guardar en DB
    cursor.execute(
        "INSERT INTO salonp (channel_id, owner_id) VALUES (%s, %s)",
        (channel.id, interaction.user.id)
    )
    cursor.execute(
        "INSERT INTO salonp_members (channel_id, user_id) VALUES (%s, %s)",
        (channel.id, interaction.user.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"🏠 Salón **{nombre}** creado correctamente.",
        ephemeral=True
    )

    await channel.send(
        f"👋 {interaction.user.mention} creó este salón privado.\n"
        "Usa `/salonp invite @usuario` para invitar."
    )

# ==========================
# /salonp invite
# ==========================

@salonp_group.command(
    name="invite",
    description="Invita a un usuario a tu salón"
)
async def salonp_invite(interaction: discord.Interaction, usuario: discord.Member):
    cursor.execute(
        "SELECT channel_id FROM salonp WHERE owner_id=%s",
        (interaction.user.id,)
    )
    result = cursor.fetchone()

    if not result:
        await interaction.response.send_message(
            "❌ No eres dueño de ningún salón.",
            ephemeral=True
        )
        return

    channel_id = result[0]
    channel = interaction.guild.get_channel(channel_id)

    if not channel:
        await interaction.response.send_message(
            "❌ El salón ya no existe.",
            ephemeral=True
        )
        return

    # Evitar duplicados
    cursor.execute(
        "SELECT 1 FROM salonp_members WHERE channel_id=%s AND user_id=%s",
        (channel_id, usuario.id)
    )
    if cursor.fetchone():
        await interaction.response.send_message(
            "⚠️ Ese usuario ya está en el salón.",
            ephemeral=True
        )
        return

    await channel.set_permissions(
        usuario,
        view_channel=True,
        send_messages=True
    )

    cursor.execute(
        "INSERT INTO salonp_members (channel_id, user_id) VALUES (%s, %s)",
        (channel_id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ {usuario.mention} fue invitado al salón.",
        ephemeral=True
    )

# ==========================
# /salonp eliminate
# ==========================

@salonp_group.command(
    name="eliminate",
    description="Elimina a un usuario de tu salón"
)
async def salonp_eliminate(interaction: discord.Interaction, usuario: discord.Member):
    cursor.execute(
        "SELECT channel_id FROM salonp WHERE owner_id=%s",
        (interaction.user.id,)
    )
    result = cursor.fetchone()

    if not result:
        await interaction.response.send_message(
            "❌ No eres dueño de ningún salón.",
            ephemeral=True
        )
        return

    channel_id = result[0]
    channel = interaction.guild.get_channel(channel_id)

    if not channel:
        await interaction.response.send_message(
            "❌ El salón no existe.",
            ephemeral=True
        )
        return

    await channel.set_permissions(usuario, overwrite=None)

    cursor.execute(
        "DELETE FROM salonp_members WHERE channel_id=%s AND user_id=%s",
        (channel_id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"🗑 {usuario.mention} fue eliminado del salón.",
        ephemeral=True
    )

import discord
from discord import app_commands
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ La variable de entorno DATABASE_URL no está configurada")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

# 🔹 ID del foro de los salones privados
from config import SALONP_FORUM_ID  # solo el ID, no conn ni cursor

# -------------------
# COMANDO: Crear salón privado
# -------------------
@app_commands.command(
    name="create",
    description="Crea un salón privado en el foro"
)
async def salonp_create(interaction: discord.Interaction, nombre: str):
    guild = interaction.guild
    forum = guild.get_channel(SALONP_FORUM_ID)

    if not forum:
        await interaction.response.send_message(
            "❌ Foro de salones no encontrado.",
            ephemeral=True
        )
        return

    try:
        # 🔹 Crear el thread con mensaje inicial
        thread_created = await forum.create_thread(
            name=nombre,
            content=f"👋 {interaction.user.mention} creó este salón privado.",
            auto_archive_duration=1440  # Archivar después de 24h
        )

        # 🔹 Obtener ThreadChannel real para poder usar add_user
        thread = await guild.fetch_channel(thread_created.id)

        # 🔒 Dar acceso al creador y administradores
        await thread.add_user(interaction.user)
        for member in guild.members:
            if member.guild_permissions.administrator:
                await thread.add_user(member)

        # 💾 Guardar en DB
        cursor.execute(
            """
            INSERT INTO salonp (thread_id, owner_id)
            VALUES (%s, %s)
            """,
            (thread.id, interaction.user.id)
        )
        cursor.execute(
            """
            INSERT INTO salonp_members (thread_id, user_id)
            VALUES (%s, %s)
            """,
            (thread.id, interaction.user.id)
        )
        conn.commit()

        await interaction.response.send_message(
            f"🏠 Salón **{nombre}** creado con éxito.",
            ephemeral=True
        )

        # Mensaje inicial en el thread
        await thread.send(
            f"👋 Bienvenido {interaction.user.mention}\n"
            "Usa `/salonp invite @usuario` para invitar."
        )

    except discord.HTTPException as e:
        await interaction.response.send_message(
            f"❌ No se pudo crear el salón: {e}",
            ephemeral=True
        )


# -------------------
# COMANDO: Invitar usuario
# -------------------
@app_commands.command(
    name="invite",
    description="Invita a un usuario a tu salón privado"
)
async def salonp_invite(interaction: discord.Interaction, usuario: discord.Member):
    cursor.execute(
        "SELECT thread_id FROM salonp WHERE owner_id = %s",
        (interaction.user.id,)
    )
    result = cursor.fetchone()

    if not result:
        await interaction.response.send_message(
            "❌ No eres dueño de ningún salón privado.",
            ephemeral=True
        )
        return

    thread_id = result[0]
    thread = interaction.guild.get_thread(thread_id)
    if not thread:
        await interaction.response.send_message(
            "❌ El salón no existe.",
            ephemeral=True
        )
        return

    await thread.add_user(usuario)

    cursor.execute(
        "INSERT INTO salonp_members (thread_id, user_id) VALUES (%s, %s)",
        (thread_id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ Usuario {usuario.mention} invitado al salón.",
        ephemeral=True
    )


# -------------------
# COMANDO: Eliminar usuario
# -------------------
@app_commands.command(
    name="eliminate",
    description="Elimina a un usuario de tu salón privado"
)
async def salonp_eliminate(interaction: discord.Interaction, usuario: discord.Member):
    cursor.execute(
        "SELECT thread_id FROM salonp WHERE owner_id = %s",
        (interaction.user.id,)
    )
    result = cursor.fetchone()

    if not result:
        await interaction.response.send_message(
            "❌ No eres dueño de ningún salón privado.",
            ephemeral=True
        )
        return

    thread_id = result[0]
    thread = interaction.guild.get_thread(thread_id)
    if not thread:
        await interaction.response.send_message(
            "❌ El salón no existe.",
            ephemeral=True
        )
        return

    await thread.remove_user(usuario)

    cursor.execute(
        "DELETE FROM salonp_members WHERE thread_id = %s AND user_id = %s",
        (thread_id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ Usuario {usuario.mention} eliminado del salón.",
        ephemeral=True
    )

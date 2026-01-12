# comands/salonp/salonp_commands.py
import discord
from discord import app_commands
from database.db import conn, cursor
from config import SALONP_FORUM_ID

# ------------------------------
# Crear salón privado
# ------------------------------
async def salonp_create(interaction: discord.Interaction, nombre: str):
    guild = interaction.guild
    forum = guild.get_channel(SALONP_FORUM_ID)

    if not forum:
        await interaction.response.send_message(
            "❌ Foro de salones no encontrado.",
            ephemeral=True
        )
        return

    # Crear thread en el foro
    thread = await forum.create_thread(
        name=nombre,
        auto_archive_duration=1440  # 24 horas, opcional
    )

    # Agregar al propietario
    await thread.add_user(interaction.user)

    # Agregar a los administradores
    for member in guild.members:
        if member.guild_permissions.administrator:
            await thread.add_user(member)

    # Guardar en la DB
    cursor.execute(
        "INSERT INTO salonp (thread_id, owner_id) VALUES (?, ?)",
        (thread.id, interaction.user.id)
    )
    cursor.execute(
        "INSERT INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
        (thread.id, interaction.user.id)
    )
    conn.commit()

    # Mensajes de confirmación
    await interaction.response.send_message(
        f"🏠 Salón **{nombre}** creado con éxito.",
        ephemeral=True
    )

    await thread.send(
        f"👋 Bienvenido {interaction.user.mention}\n"
        "Usa `/salonp invite @usuario` para invitar a otros."
    )

# ------------------------------
# Invitar a un usuario
# ------------------------------
async def salonp_invite(interaction: discord.Interaction, usuario: discord.Member):
    guild = interaction.guild

    # Buscar thread en la DB donde el usuario es propietario
    cursor.execute(
        "SELECT thread_id FROM salonp WHERE owner_id = ?",
        (interaction.user.id,)
    )
    result = cursor.fetchone()
    if not result:
        await interaction.response.send_message(
            "❌ No tienes un salón privado creado.",
            ephemeral=True
        )
        return

    thread_id = result[0]
    thread = guild.get_channel(thread_id)
    if not thread:
        await interaction.response.send_message(
            "❌ Salón no encontrado.",
            ephemeral=True
        )
        return

    # Agregar al usuario
    await thread.add_user(usuario)

    # Guardar en DB
    cursor.execute(
        "INSERT INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
        (thread.id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ {usuario.mention} ha sido invitado a tu salón.",
        ephemeral=True
    )
    await thread.send(f"👤 {usuario.mention} se ha unido al salón.")

# ------------------------------
# Eliminar salón privado
# ------------------------------
async def salonp_eliminate(interaction: discord.Interaction):
    guild = interaction.guild

    # Buscar thread en la DB donde el usuario es propietario
    cursor.execute(
        "SELECT thread_id FROM salonp WHERE owner_id = ?",
        (interaction.user.id,)
    )
    result = cursor.fetchone()
    if not result:
        await interaction.response.send_message(
            "❌ No tienes un salón privado creado.",
            ephemeral=True
        )
        return

    thread_id = result[0]
    thread = guild.get_channel(thread_id)
    if thread:
        await thread.delete()

    # Borrar de la DB
    cursor.execute(
        "DELETE FROM salonp_members WHERE thread_id = ?",
        (thread_id,)
    )
    cursor.execute(
        "DELETE FROM salonp WHERE thread_id = ?",
        (thread_id,)
    )
    conn.commit()

    await interaction.response.send_message(
        "🗑️ Tu salón privado ha sido eliminado.",
        ephemeral=True
    )

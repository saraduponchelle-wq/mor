# comands/salonp/salonp_commands.py
import discord
from discord import app_commands
from config import SALONP_FORUM_ID
from database.db import conn, cursor

# -------------------
# COMANDO: Crear salón
# -------------------
@app_commands.command(
    name="create",
    description="Crea un salón privado en el foro"
)
@app_commands.describe(nombre="Nombre del salón privado")
async def salonp_create(interaction: discord.Interaction, nombre: str):
    # Validar que el nombre no esté vacío
    if not nombre.strip():
        await interaction.response.send_message(
            "❌ Debes especificar un nombre válido para el salón.",
            ephemeral=True
        )
        return

    guild = interaction.guild
    forum = guild.get_channel(SALONP_FORUM_ID)

    if not forum:
        await interaction.response.send_message(
            "❌ Foro de salones no encontrado.",
            ephemeral=True
        )
        return

    try:
        # 🔍 Crear thread privado
        thread = await forum.create_thread(
            name=nombre,
            type=discord.ChannelType.private_thread
        )

        # 🔒 Agregar al creador y administradores
        await thread.add_user(interaction.user)
        for member in guild.members:
            if member.guild_permissions.administrator:
                await thread.add_user(member)

        # 💾 Guardar en DB
        cursor.execute(
            "INSERT INTO salonp (thread_id, owner_id) VALUES (?, ?)",
            (thread.id, interaction.user.id)
        )
        cursor.execute(
            "INSERT INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
            (thread.id, interaction.user.id)
        )
        conn.commit()

        # ✅ Mensaje de éxito al usuario
        await interaction.response.send_message(
            f"🏠 Salón **{nombre}** creado con éxito.",
            ephemeral=True
        )

        # 👋 Mensaje de bienvenida en el thread
        await thread.send(
            content=f"👋 Bienvenido {interaction.user.mention}!\n"
                    "Usa `/salonp invite @usuario` para invitar a alguien al salón."
        )

    except discord.HTTPException as e:
        # Manejar errores de Discord (p. ej. permisos insuficientes)
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
        "SELECT thread_id FROM salonp WHERE owner_id = ?",
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
        "INSERT INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
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
        "SELECT thread_id FROM salonp WHERE owner_id = ?",
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
        "DELETE FROM salonp_members WHERE thread_id = ? AND user_id = ?",
        (thread_id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ Usuario {usuario.mention} eliminado del salón.",
        ephemeral=True
    )

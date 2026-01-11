import discord
from discord import app_commands
from config import SALONP_FORUM_ID
from database.db import conn, cursor

async def salonp_create(interaction: discord.Interaction, nombre: str):
    guild = interaction.guild
    forum = guild.get_channel(SALONP_FORUM_ID)

    if not forum:
        await interaction.response.send_message(
            "❌ Foro de salones no encontrado.",
            ephemeral=True
        )
        return

    # 🔍 Crear thread privado
    thread = await forum.create_thread(
        name=nombre,
        type=discord.ChannelType.private_thread
    )

    # 🔒 Dar permisos
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

    # ✅ Mensaje final
    await interaction.response.send_message(
        f"🏠 Salón **{nombre}** creado con éxito.",
        ephemeral=True
    )

    await thread.send(
        f"👋 Bienvenido {interaction.user.mention}\n"
        "Usa `/salonP invite @usuario` para invitar."
    )

# 🌟 Crear comando de app_commands
create_command = app_commands.Command(
    name="create",
    description="Crea un chat privado en el foro",
    callback=salonp_create
)

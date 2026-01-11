import discord
from discord import app_commands
from database.db import conn, cursor

async def salonp_invite(interaction: discord.Interaction, usuario: discord.Member):
    guild = interaction.guild
    thread = interaction.channel

    # 🔍 Verificar que sea un thread en nuestra DB
    cursor.execute("SELECT owner_id FROM salonp WHERE thread_id = ?", (thread.id,))
    result = cursor.fetchone()
    if not result:
        await interaction.response.send_message(
            "❌ Este canal no es un salón registrado.",
            ephemeral=True
        )
        return

    owner_id = result[0]

    # Solo el dueño o admins pueden invitar
    if interaction.user.id != owner_id and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permisos para invitar a este salón.",
            ephemeral=True
        )
        return

    # 🔒 Dar acceso al usuario
    await thread.add_user(usuario)

    # 💾 Guardar en DB
    cursor.execute(
        "INSERT OR IGNORE INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
        (thread.id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ {usuario.mention} ahora puede acceder al salón.",
        ephemeral=True
    )

# 🌟 Crear comando
invite_command = app_commands.Command(
    name="invite",
    description="Invita a alguien a tu salón privado",
    callback=salonp_invite
)

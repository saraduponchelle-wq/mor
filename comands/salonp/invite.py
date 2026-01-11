import discord
from discord import app_commands
from database.db import conn, cursor
from commands.salonp import salonp_group


@salonp_group.command(
    name="invite",
    description="Invita a un usuario a tu salón privado"
)
async def salonp_invite(
    interaction: discord.Interaction,
    usuario: discord.Member
):
    canal = interaction.channel

    # ❌ Debe ser un thread
    if not isinstance(canal, discord.Thread):
        await interaction.response.send_message(
            "❌ Este comando solo puede usarse dentro de un salón.",
            ephemeral=True
        )
        return

    # 🔍 Verificar que es un salón registrado
    cursor.execute(
        "SELECT owner_id FROM salonp WHERE thread_id = ?",
        (canal.id,)
    )
    data = cursor.fetchone()

    if not data:
        await interaction.response.send_message(
            "❌ Este canal no es un salón privado.",
            ephemeral=True
        )
        return

    owner_id = data[0]

    # 👑 Solo owner o admin
    if interaction.user.id != owner_id and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permiso para invitar usuarios.",
            ephemeral=True
        )
        return

    # 🚫 Ya está dentro
    cursor.execute(
        "SELECT 1 FROM salonp_members WHERE thread_id = ? AND user_id = ?",
        (canal.id, usuario.id)
    )
    if cursor.fetchone():
        await interaction.response.send_message(
            "⚠️ Ese usuario ya está en el salón.",
            ephemeral=True
        )
        return

    # ➕ Añadir al thread
    await canal.add_user(usuario)

    # 💾 Guardar en DB
    cursor.execute(
        "INSERT INTO salonp_members (thread_id, user_id) VALUES (?, ?)",
        (canal.id, usuario.id)
    )
    conn.commit()

    await interaction.response.send_message(
        f"✅ {usuario.mention} fue invitado al salón."
    )

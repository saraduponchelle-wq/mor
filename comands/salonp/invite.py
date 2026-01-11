# comands/salonp/invite.py
import discord
from discord import app_commands
from database.db import conn, cursor

@app_commands.command(name="salonp_invite", description="Invita a alguien a tu chat privado")
async def salonp_invite(interaction: discord.Interaction, usuario: discord.Member):
    guild = interaction.guild
    thread_id = cursor.execute(
        "SELECT thread_id FROM salonp WHERE owner_id = ?", (interaction.user.id,)
    ).fetchone()

    if not thread_id:
        await interaction.response.send_message(
            "❌ No tienes un salón activo.",
            ephemeral=True
        )
        return

    thread_id = thread_id[0]
    thread = guild.get_channel(thread_id)

    if not thread:
        await interaction.response.send_message(
            "❌ No se encontró tu thread.",
            ephemeral=True
        )
        return

    # Revisar si ya está invitado
    already = cursor.execute(
        "SELECT 1 FROM salonp_members WHERE thread_id = ? AND user_id = ?",
        (thread_id, usuario.id)
    ).fetchone()

    if already:
        await interaction.response.send_message(
            f"ℹ️ {usuario.mention} ya tiene acceso a tu salón.",
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
        f"✅ {usuario.mention} ha sido invitado a tu salón privado.",
        ephemeral=True
    )

    await thread.send(f"👋 {usuario.mention} ha sido invitado por {interaction.user.mention}.")

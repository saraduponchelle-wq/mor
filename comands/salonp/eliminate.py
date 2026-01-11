# comands/salonp/eliminate.py
import discord
from discord import app_commands
from database.db import conn, cursor

@app_commands.command(name="salonp_eliminate", description="Elimina tu chat privado")
async def salonp_eliminate(interaction: discord.Interaction):
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

    if thread:
        await thread.delete()

    # Limpiar DB
    cursor.execute("DELETE FROM salonp_members WHERE thread_id = ?", (thread_id,))
    cursor.execute("DELETE FROM salonp WHERE thread_id = ?", (thread_id,))
    conn.commit()

    await interaction.response.send_message(
        "🗑️ Tu salón privado ha sido eliminado.",
        ephemeral=True
    )

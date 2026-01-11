import discord
from discord import app_commands
from database.db import conn, cursor

async def salonp_eliminate(interaction: discord.Interaction):
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

    # Solo el dueño o admins pueden eliminar
    if interaction.user.id != owner_id and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ No tienes permisos para eliminar este salón.",
            ephemeral=True
        )
        return

    # 💾 Eliminar de la DB
    cursor.execute("DELETE FROM salonp WHERE thread_id = ?", (thread.id,))
    cursor.execute("DELETE FROM salonp_members WHERE thread_id = ?", (thread.id,))
    conn.commit()

    # 🗑️ Eliminar thread
    await thread.delete()

    await interaction.response.send_message(
        "✅ Salón eliminado con éxito.",
        ephemeral=True
    )

# 🌟 Crear comando
eliminate_command = app_commands.Command(
    name="eliminate",
    description="Elimina tu salón privado",
    callback=salonp_eliminate
)

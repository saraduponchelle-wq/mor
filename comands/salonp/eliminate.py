import discord
from discord import app_commands
from database.db import conn, cursor
from commands.salonp import salonp_group


@salonp_group.command(
    name="eliminate",
    description="Elimina tu salón privado"
)
async def salonp_eliminate(interaction: discord.Interaction):
    canal = interaction.channel

    # ❌ Debe ser un thread
    if not isinstance(canal, discord.Thread):
        await interaction.response.send_message(
            "❌ Este comando solo puede usarse dentro de un salón.",
            ephemeral=True
        )
        return

    # 🔍 Verificar salón
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

    # 👑 Solo dueño o admin
    if interaction.user.id != owner_id and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Solo el creador o un admin puede eliminar este salón.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "🗑️ Eliminando el salón..."
    )

    # 🧹 Limpiar DB
    cursor.execute(
        "DELETE FROM salonp_members WHERE thread_id = ?",
        (canal.id,)
    )
    cursor.execute(
        "DELETE FROM salonp WHERE thread_id = ?",
        (canal.id,)
    )
    conn.commit()

    # 💥 Borrar canal
    await canal.delete(reason="Salón privado eliminado")

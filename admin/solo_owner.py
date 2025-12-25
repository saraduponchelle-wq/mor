import discord
from discord import app_commands

OWNER_ID = 903114752060977202

@app_commands.command(
    name="solo_owner",
    description="Comando exclusivo de la creadora"
)
async def solo_owner(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ No tienes permiso para usar esto.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "👑✨ Mi reina ha dado una orden.",
        ephemeral=True
    )

import discord
from discord import app_commands

OWNER_ID = 903114752060977202

@app_commands.command(name="diversion", description="Activa o desactiva el modo diversión")
async def diversion(interaction: discord.Interaction):

    bot = interaction.client

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("No puedes usar este comando.", ephemeral=True)
        return

    bot.diversion_activo = not bot.diversion_activo

    estado = "activado 🎉" if bot.diversion_activo else "desactivado ❌"

    await interaction.response.send_message(f"Modo diversión {estado}")
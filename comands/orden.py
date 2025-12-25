import discord
from discord import app_commands

EMOJI_JIJI = "<:jiji:1451013733513035920>"

@app_commands.command(name="orden", description="Muestra el orden de jugadores")
async def orden(interaction: discord.Interaction):
    jugadores = interaction.client.jugadores

    if not jugadores:
        await interaction.response.send_message("❌ No hay jugadores.")
        return

    texto = f"{EMOJI_JIJI} **Orden de jugadores:**\n\n"
    for i, j in enumerate(jugadores, 1):
        texto += f"{i}. {j.mention}\n"

    await interaction.response.send_message(texto)

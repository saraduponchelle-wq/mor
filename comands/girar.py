import discord
from discord import app_commands
import random

EMOJI_RANDOM = "<a:random:1451014515473911828>"

@app_commands.command(name="girar", description="Gira la ruleta")
async def girar(interaction: discord.Interaction):
    jugadores = interaction.client.jugadores

    if not jugadores:
        await interaction.response.send_message("❌ No hay jugadores.")
        return

    elegido = random.choice(jugadores)
    await interaction.response.send_message(
        f"{EMOJI_RANDOM} 🎯 Jugador elegido: {elegido.mention}"
    )

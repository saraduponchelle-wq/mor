import discord
from discord import app_commands
import random
import os

EMOJI_RANDOM = "<a:random:1451014515473911828>"

@app_commands.command(name="reto", description="Reto aleatorio")
async def reto(interaction: discord.Interaction):
    carpeta = "retos"

    if not os.path.exists(carpeta):
        await interaction.response.send_message("❌ No hay retos.")
        return

    imagen = random.choice(os.listdir(carpeta))

    await interaction.response.send_message(
        f"{EMOJI_RANDOM} **Reto seleccionado:**",
        file=discord.File(os.path.join(carpeta, imagen))
    )

import discord
from discord import app_commands
import random
import os

EMOJI_JIJI = "<:jiji:1451013733513035920>"

@app_commands.command(name="adorar", description="Honrar a Mor")
async def adorar(interaction: discord.Interaction):
    carpeta = "Mor"

    if not os.path.exists(carpeta):
        await interaction.response.send_message("❌ No hay imágenes.")
        return

    imagen = random.choice(os.listdir(carpeta))

    await interaction.response.send_message(
        f"🕯️ {EMOJI_JIJI} **Todos adoramos a la diosa Mor.**",
        file=discord.File(os.path.join(carpeta, imagen))
    )

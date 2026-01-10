import discord
from discord import app_commands
import os
import random

OWNER_ID = 903114752060977202  # Solo tú puedes usar este comando
SPECIAL_ID = 823625858795307028  # Persona para beso en los labios

BESOS_COMUNES = [
    "💌 Un beso viajero ha sido enviado…",
    "🌬️ Siente el viento del cariño…",
    "😘 Un dulce beso a la distancia."
]

BESO_MOR = [
    "💖 Solo Mor puede enviar este beso especial…",
    "💫 La suerte de Mor te toca con un beso."
]

@app_commands.command(name="beso", description="Envía un beso a alguien")
@app_commands.describe(usuario="El usuario al que quieres enviar un beso")
async def beso(interaction: discord.Interaction, usuario: discord.Member):
    # ❌ Comprobar si el que usa el comando es el OWNER
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ Solo el dueño del comando puede enviar besos.",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    # Determinar el gif y el comentario
    if usuario.id == SPECIAL_ID:
        gif_path = "Mor/kiss.gif"
        comentario = "💋 Un beso en los labios ha sido enviado…"
    else:
        gif_path = "Mor/aire.gif"
        comentario = random.choice(BESO_MOR if interaction.user.id == OWNER_ID else BESOS_COMUNES)

    # Crear embed
    embed_beso = discord.Embed(
        title="💌 ¡Beso enviado!",
        description=f"{comentario}\n\n👤 **De:** {interaction.user.mention}\n👤 **Para:** {usuario.mention}",
        color=discord.Color.pink()
    )
    embed_beso.set_image(url=f"attachment://{os.path.basename(gif_path)}")

    # Enviar embed con gif
    await interaction.followup.send(
        embed=embed_beso,
        file=discord.File(gif_path, filename=os.path.basename(gif_path))
    )

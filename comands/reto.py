import discord
from discord import app_commands
import random
import os
import asyncio

EMOJI_RANDOM = "<a:random:1451014515473911828>"
MOR_ID = 903114752060977202

COMENTARIOS = [
    "✨ El destino ya habló… no intentes escapar.",
    "🎭 Qué giro tan interesante~",
    "😈 Ohhh~ esto va a ser divertido.",
    "🎲 El caos sonríe con esta elección.",
    "💫 La suerte jamás se equivoca… ¿o sí?"
]

COMENTARIOS_MOR = [
    "👑 La ruleta se inclina ante su creadora.",
    "✨ El destino hace reverencia.",
    "😌 Oh~ cuando tú giras la ruleta, el caos se ordena.",
    "💖 Incluso la suerte sabe quién manda aquí."
]

@app_commands.command(name="reto", description="Gira la ruleta del reto")
async def reto(interaction: discord.Interaction):

    await interaction.response.defer()

    carpeta = "retos"
    if not os.path.exists(carpeta) or not os.listdir(carpeta):
        await interaction.followup.send("❌ No hay retos disponibles.")
        return

    # 🎰 EMBED DE RULETA
    embed_ruleta = discord.Embed(
        title="🎰 Girando la ruleta del reto…",
        description=(
            f"{EMOJI_RANDOM} *Trin~ trin~ trin~*\n\n"
            "La ruleta gira sin piedad…\n"
            "El destino está a punto de decidir."
        ),
        color=discord.Color.gold()
    )
    embed_ruleta.set_image(url="attachment://ruleta.gif")

    mensaje_ruleta = await interaction.followup.send(
        embed=embed_ruleta,
        file=discord.File("Mor/ruleta.gif", filename="ruleta.gif"),
        wait=True
    )

    # ⏳ Espera dramática
    await asyncio.sleep(4)

    # 🗑️ Borrar ruleta
    await mensaje_ruleta.delete()

    # 🎯 Elegir reto
    imagen = random.choice(os.listdir(carpeta))
    comentario = (
        random.choice(COMENTARIOS_MOR)
        if interaction.user.id == MOR_ID
        else random.choice(COMENTARIOS)
    )

    embed_reto = discord.Embed(
        title="🎯 RETO SELECCIONADO",
        description=(
            f"{comentario}\n\n"
            f"👤 **Jugador:** {interaction.user.mention}"
        ),
        color=discord.Color.purple()
    )

    embed_reto.set_image(url=f"attachment://{imagen}")

    await interaction.followup.send(
        embed=embed_reto,
        file=discord.File(os.path.join(carpeta, imagen), filename=imagen)
    )

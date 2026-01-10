import discord
from discord import app_commands
import random
import os

EMOJI_JIJI = "<:jiji:1451013733513035920>"
MOR_ID = 903114752060977202

@app_commands.command(name="adorar", description="Honrar a Mor")
async def adorar(interaction: discord.Interaction):

    gifs = ["love.gif", "beauty.gif"]
    elegido = random.choice(gifs)

    ruta_gif = f"Mor/{elegido}"

    if not os.path.exists(ruta_gif):
        await interaction.response.send_message("❌ El ritual falló… no hay ofrenda.")
        return

    # 💗 LOVE.GIF
    if elegido == "love.gif":
        embed = discord.Embed(
            title="💖 Un acto de devoción absoluta 💖",
            description=(
                f"{EMOJI_JIJI} *Ohhh~ qué escena tan preciosa…*\n\n"
                f"El amor se desborda, los corazones tiemblan y **Mor** recibe "
                f"otra ofrenda digna de admiración eterna.\n\n"
                f"<@{MOR_ID}> ✨"
            ),
            color=discord.Color.from_rgb(255, 105, 180)  # Rosa intenso
        )

        embed.set_image(url="attachment://love.gif")

        await interaction.response.send_message(
            embed=embed,
            file=discord.File(ruta_gif, filename="love.gif")
        )

        mensaje = await interaction.original_response()

        # Reacciones estilo Sparkle
        for emoji in ["💖", "💝", "🎁", "✨"]:
            await mensaje.add_reaction(emoji)

    # 🎶 BEAUTY.GIF
    else:
        embed = discord.Embed(
            title="✨ Belleza que roba el aliento ✨",
            description=(
                f"{EMOJI_JIJI} *Shhh… observa con atención.*\n\n"
                f"La elegancia, la presencia, la perfección misma se manifiesta.\n"
                f"No todos pueden apreciarlo… pero **Mor** sí.\n\n"
                f"<@{MOR_ID}> 💫"
            ),
            color=discord.Color.purple()
        )

        embed.set_image(url="attachment://beauty.gif")

        await interaction.response.send_message(
            embed=embed,
            file=discord.File(ruta_gif, filename="beauty.gif")
        )

        # Enviar canción después
        await interaction.followup.send(
            file=discord.File("Mor/song.mp3")
        )

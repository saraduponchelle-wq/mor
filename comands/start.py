import discord
from discord import app_commands

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"
CANAL_NOTICIAS_ID = 1451664597843968111

@app_commands.command(name="start", description="Inicia la ruleta")
async def start(interaction: discord.Interaction):
    bot = interaction.client
    bot.jugadores.clear()

    embed = discord.Embed(
        title="🎰 ¡Juego de Ruleta Iniciado!",
        description=(
            f"{EMOJI_RANDOM} La suerte comienza a girar…\n\n"
            f"{EMOJI_JIJI} **Reacciona con 🎉 para unirte al juego.**"
        ),
        color=discord.Color.red()
    )

    embed.set_image(url="attachment://anuncio.gif")

    await interaction.response.send_message(
        embed=embed,
        file=discord.File("Mor/anuncio.gif", filename="anuncio.gif")
    )

    bot.mensaje_registro = await interaction.original_response()
    await bot.mensaje_registro.add_reaction("🎉")

    canal = interaction.guild.get_channel(CANAL_NOTICIAS_ID)
    if canal:
        await canal.send(
            "@everyone 🎰 **¡La ruleta ha comenzado!**\n"
            "Ve al canal del juego y participa."
        )

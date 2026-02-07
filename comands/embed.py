import discord
from discord import app_commands
import os

@app_commands.command(name="eventoamor", description="Muestra la información del evento de San Valentín")
async def evento_amor(interaction: discord.Interaction):

    # Respuesta silenciosa para cumplir con Discord
    await interaction.response.defer()

    # 1️⃣ @everyone
    await interaction.channel.send("@everyone")

    # 2️⃣ GIF
    await interaction.channel.send(file=discord.File("images/embed.gif"))

    # 3️⃣ Embed
    embed = discord.Embed(
        title="💞 EVENTO SAN VALENTÍN – TÍTULOS ESPECIALES ✨🏹",
        description=(
            "*El amor ya está flotando en el aire…*\n"
            "*¿Estás listo para convertirlo en destino? 🏹💕*\n\n"
            "Este año podrás conseguir títulos exclusivos cumpliendo ciertos rituales románticos… 🤲💖"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )

    embed.add_field(
        name="💌🏹 Título: @💘 Certified by Cupid",
        value=(
            "**Para obtenerlo deberás:**\n\n"
            "💞 Usar `/sanvalentin` y que tu persona especial acepte tu invitación.\n"
            "💞 Hacer una confesión pública usando `/confesion`.\n"
            "💞 Tener una cita en un canal de rol y ponerte un match.\n"
            "💞 Participar en la votación del día 13.\n\n"
            "**Cuando cumplas TODO:**\n"
            "✨ Envía la palabra **“Terminado”**\n"
            "✨ Adjunta las capturas\n"
            "✨ Mándalo al canal #Redeem\n\n"
            "Y el destino decidirá… 💫"
        ),
        inline=False
    )

    embed.add_field(
        name="👑💖 Título: @💖 Almas Gemelas",
        value=(
            "Solo para quienes brillen más que las estrellas… 💫\n\n"
            "**Requisitos:**\n"
            "💞 Ponerte un match con tu persona especial.\n"
            "💞 Enviar las dos imágenes del match al canal #concurso.\n"
            "💞 Participar en la votación del día 13.\n"
            "💞 Ganar el concurso del match más lindo.\n\n"
            "La pareja elegida será coronada como la más adorable del reino 💗✨"
        ),
        inline=False
    )

    embed.add_field(
        name="🌸✨ Mensaje de Mor",
        value=(
            "Hi hi, lovely souls~ 🌸✨\n\n"
            "El amor no es una casualidad…\n"
            "es una pequeña chispa brillante que decide nacer en el momento perfecto.\n\n"
            "Cada latido guarda una historia,\n"
            "cada sonrisa puede convertirse en un recuerdo eterno.\n\n"
            "Que este San Valentín florezcan confesiones sinceras,\n"
            "encuentros destinados\n"
            "y corazones que brillen un poquito más fuerte que ayer 💞🌷\n\n"
            "Con cariño…\n"
            "Mor, la diosa del amor 💘"
        ),
        inline=False
    )

    await interaction.followup.send(embed=embed)

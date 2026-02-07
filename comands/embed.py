import discord
from discord import app_commands
import os

@app_commands.command(name="eventoamor", description="Muestra la información del evento de San Valentín")
async def evento_amor(interaction: discord.Interaction):

    # Respuesta silenciosa
    await interaction.response.defer()

    # 1️⃣ everyone
    await interaction.channel.send("@everyone")

    # 2️⃣ gif
    await interaction.channel.send(file=discord.File("images/embed.gif"))

    # 3️⃣ embed con EXACTA estructura
    embed = discord.Embed(
        description=(
            "***:heartdecor:  EVENTO SAN VALENTÍN – TÍTULOS ESPECIALES :sparkles::cupid:***\n\n"

            "*El amor ya está flotando en el aire…*\n"
            "*¿Estás listo para convertirlo en destino? :bow_and_arrow::two_hearts:*\n\n"

            "Este año podrás conseguir títulos exclusivos cumpliendo ciertos rituales románticos…:corazonmano:\n\n"

            "══════════════════════════════════════════\n"
            "✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ .\n"
            "︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧\n\n"

            "***:love_letter::bow_and_arrow: Título: <@&ROLE_ID_CUPIDO> ***\n\n"

            "> *Para obtenerlo deberás:*\n> \n"
            "> :heartdecor:  Usar el comando `/sanvalentin` y que tu persona especial acepte tu invitación. :lesbianlove:\n"
            "> :heartdecor: Hacer una confesión pública a esa persona especial usando `/confesion`.\n"
            "> :heartdecor: Tener una cita en alguno de los canales de rol y ponerte un match con esa persona. :idea:\n"
            "> :heartdecor: Participar en la votación del día 13 para el concurso del match más bonito.\n> \n"
            "> *Cuando hayas cumplido TODO:*\n> \n"
            "> :sparkles: Envía la palabra “Terminado”\n"
            "> :sparkles: Adjunta las capturas\n"
            "> :sparkles: Mándalo al canal https://discord.com/channels/1447694785551929490/1469466985925705951 :write:\n> \n"
            "> Y el destino decidirá… :dizzy:\n\n"

            "✦•·································•⊹₊˚‧︵‿₊୨ᰔ୧₊‿︵‧˚₊⊹ •·································•✦\n\n"

            "**:crown::revolving_hearts: Título: <@&ROLE_ID_ALMAS> **\n\n"

            "> Este es solo para quienes brillen más que las estrellas… :AMOR:\n> \n"
            "> *Requisitos:*\n> \n"
            "> :heartdecor: Ponerte un match con tu persona especial. :corazonmano:\n"
            "> :heartdecor: Enviar las dos imágenes del match al canal https://discord.com/channels/1447694785551929490/1469466703766491309\n"
            "> :heartdecor: El día 13 se hará una votación. :like:\n"
            "> :heartdecor: Ganar el concurso del match más lindo.\n\n"
            "> La pareja elegida será coronada como la más adorable del reino :sparkling_heart::sparkles:\n\n"

            "✦•·································•⊹₊˚‧︵‿₊୨ᰔ୧₊‿︵‧˚₊⊹ •·································•✦\n\n"

            ":heartdecor: Hi hi, lovely souls~ :cherry_blossom::sparkles:\n\n"

            "> El amor no es una casualidad…\n"
            "> es una pequeña chispa brillante que decide nacer en el momento perfecto.\n> \n"
            "> Cada latido guarda una historia,\n"
            "> cada sonrisa puede convertirse en un recuerdo eterno.\n> \n"
            "> Que este San Valentín florezcan confesiones sinceras,\n"
            "> encuentros destinados\n"
            "> y corazones que brillen un poquito más fuerte que ayer :revolving_hearts::tulip:\n> \n"
            "> Con cariño…\n"
            "> Mor, la diosa del amor :pretty:"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )

    await interaction.channel.send(embed=embed)

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
            "***<:heartdecor:1469474857631748137>  EVENTO SAN VALENTÍN – TÍTULOS ESPECIALES :sparkles::cupid:***\n\n"

            "*El amor ya está flotando en el aire…*\n"
            "*¿Estás listo para convertirlo en destino? :bow_and_arrow::two_hearts:*\n\n"

            "Este año podrás conseguir títulos exclusivos cumpliendo ciertos rituales románticos…<:corazonmano:1469474803588006041>\n\n"

            "══════════════════════════════════════════\n"
            "✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ .\n"
            "︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧\n\n"

            "***:love_letter::bow_and_arrow: Título: <@&1468115588923654311> ***\n\n"

            "> *Para obtenerlo deberás:*\n> \n"
            "> <:heartdecor:1469474857631748137>  Usar el comando `/sanvalentin` y que tu persona especial acepte tu invitación. <:lesbianlove:1469474917845303544>\n"
            "> <:heartdecor:1469474857631748137> Hacer una confesión pública a esa persona especial usando `/confesion`.\n"
            "> <:heartdecor:1469474857631748137> Tener una cita en alguno de los canales de rol y ponerte un match con esa persona. <:idea:1469474702710935715>\n"
            "> <:heartdecor:1469474857631748137> Participar en la votación del día 13 para el concurso del match más bonito.\n> \n"
            "> *Cuando hayas cumplido TODO:*\n> \n"
            "> :sparkles: Envía la palabra “Terminado”\n"
            "> :sparkles: Adjunta las capturas\n"
            "> :sparkles: Mándalo al canal https://discord.com/channels/1447694785551929490/1469466985925705951 <:write:1469474668892258376>\n> \n"
            "> Y el destino decidirá… :dizzy:\n\n"

            "✦•·································•⊹₊˚‧︵‿₊୨ᰔ୧₊‿︵‧˚₊⊹ •·································•✦\n\n"

            "**:crown::revolving_hearts: Título: <@&1468116870833115351> **\n\n"

            "> Este es solo para quienes brillen más que las estrellas… <:AMOR:1469473509259481210>\n> \n"
            "> *Requisitos:*\n> \n"
            "> <:heartdecor:1469474857631748137> Ponerte un match con tu persona especial. <:corazonmano:1469474803588006041>\n"
            "> <:heartdecor:1469474857631748137> Enviar las dos imágenes del match al canal https://discord.com/channels/1447694785551929490/1469466703766491309\n"
            "> <:heartdecor:1469474857631748137> El día 13 se hará una votación. <:like:1469474742573465661>\n"
            "> <:heartdecor:1469474857631748137> Ganar el concurso del match más lindo.\n\n"
            "> La pareja elegida será coronada como la más adorable del reino :sparkling_heart::sparkles:\n\n"

            "✦•·································•⊹₊˚‧︵‿₊୨ᰔ୧₊‿︵‧˚₊⊹ •·································•✦\n\n"

            "<:heartdecor:1469474857631748137> Hi hi, lovely souls~ :cherry_blossom::sparkles:\n\n"

            "> El amor no es una casualidad…\n"
            "> es una pequeña chispa brillante que decide nacer en el momento perfecto.\n> \n"
            "> Cada latido guarda una historia,\n"
            "> cada sonrisa puede convertirse en un recuerdo eterno.\n> \n"
            "> Que este San Valentín florezcan confesiones sinceras,\n"
            "> encuentros destinados\n"
            "> y corazones que brillen un poquito más fuerte que ayer :revolving_hearts::tulip:\n> \n"
            "> Con cariño…\n"
            "> Mor, la diosa del amor <:pretty:1469474951387025563>"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )

    await interaction.channel.send(embed=embed)

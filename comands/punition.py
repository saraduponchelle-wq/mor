import discord
from discord import app_commands
import random
import asyncio

OWNER_ID = 903114752060977202

@app_commands.command(name="punition", description="La ruleta decide el castigo")
async def punition(interaction: discord.Interaction, usuario: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ No tienes autoridad para castigar.",
            ephemeral=True
        )
        return

    guild = interaction.guild

    # 🎰 EMBED DE RULETA
    embed_ruleta = discord.Embed(
        title="🎰 Girando la ruleta del castigo...",
        description="El destino se decide ahora.",
        color=discord.Color.red()
    )
    embed_ruleta.set_image(url="attachment://ruleta.gif")

    await interaction.response.send_message(
        embed=embed_ruleta,
        file=discord.File("Mor/ruleta.gif", filename="ruleta.gif")
    )

    mensaje_ruleta = await interaction.original_response()
    await asyncio.sleep(4)
    await mensaje_ruleta.delete()

    # 🎯 CASTIGOS DISPONIBLES
    castigos = [
        "silencio",
        "expulsion",
        "avergonzar"
    ]

    castigo = random.choice(castigos)

    # 🟢 CASTIGOS LEVES
    if castigo == "silencio":
        duration = random.randint(10, 30)

        overwrite = interaction.channel.overwrites_for(usuario)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(usuario, overwrite=overwrite)

        await asyncio.sleep(duration)

        overwrite.send_messages = None
        await interaction.channel.set_permissions(usuario, overwrite=overwrite)

        texto = f"🤫 {usuario.mention} fue silenciado por **{duration} segundos**."
        gif = "Mor/dislike.gif"

    elif castigo == "avergonzar":
        texto = f"😈 {usuario.mention} fue señalado por la ruleta. Qué vergüenza."
        gif = "Mor/dislike.gif"

    # 🔴 CASTIGO GRAVE
    else:  # expulsión
        invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)

        try:
            await usuario.send(
                "💀 Has sido expulsado por decisión de la ruleta.\n"
                f"🔗 Puedes volver aquí: {invite}"
            )
        except:
            pass

        await guild.kick(usuario, reason="Castigo de la ruleta")

        texto = f"💀 {usuario.mention} fue **expulsado del servidor**."
        gif = "Mor/castigo.gif"

    # 📢 EMBED FINAL
    embed_final = discord.Embed(
        title="⚖️ Castigo Ejecutado",
        description=texto,
        color=discord.Color.dark_red()
    )
    embed_final.set_image(url="attachment://castigo.gif")

    await interaction.followup.send(
        content=f"{usuario.mention}",
        embed=embed_final,
        file=discord.File(gif, filename="castigo.gif")
    )

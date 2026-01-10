import discord
from discord import app_commands
import random
import asyncio
import os


OWNER_ID = 903114752060977202

# 🔇 Silencio real por canal
async def silenciar_en_canal(canal: discord.TextChannel, miembro: discord.Member, segundos: int):
    overwrite = canal.overwrites_for(miembro)
    overwrite.send_messages = False
    overwrite.add_reactions = False

    try:
        await canal.set_permissions(miembro, overwrite=overwrite)
    except discord.Forbidden:
        await canal.send(f"❌ No puedo silenciar a {miembro.mention}, permisos insuficientes.")
    await asyncio.sleep(segundos)

    overwrite.send_messages = None
    overwrite.add_reactions = None
    await canal.set_permissions(miembro, overwrite=overwrite)


@app_commands.command(name="punition", description="La ruleta decide el castigo")
async def punition(interaction: discord.Interaction, usuario: discord.Member):
    # 👑 Solo el dueño
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ No tienes autoridad para castigar.",
            ephemeral=True
        )
        return

    canal = interaction.channel
    guild = interaction.guild

    # 🎰 EMBED RULETA
    embed_ruleta = discord.Embed(
        title="🎰 Girando la ruleta del castigo...",
        description="El destino está decidiendo su suerte.",
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

    # 🎯 Castigos posibles
    castigos = ["silencio", "avergonzar", "expulsion"]
    castigo = random.choice(castigos)

    # 🟢 SILENCIO
    # 🟢 SILENCIO
    if castigo == "silencio":
        duracion = random.randint(10, 30)

        # Primero enviamos el embed anunciando el castigo
        texto = (
            f"🤫 {usuario.mention} será silenciado por "
            f"**{duracion} segundos**.\n"
            "La ruleta sonríe."
        )
        gif = "Mor/dislike.gif"

        embed_final = discord.Embed(
            title="⚖️ Castigo Decidido",
            description=texto,
            color=discord.Color.green()
        )
        embed_final.set_image(url=f"attachment://{os.path.basename(gif)}")

        await canal.send(
            content=usuario.mention,
            embed=embed_final,
            file=discord.File(gif, filename=os.path.basename(gif))
        )

        # Después aplicamos el silencio
        await silenciar_en_canal(canal, usuario, duracion)


    # 🟡 AVERGONZAR
    elif castigo == "avergonzar":
        texto = (
            f"😈 {usuario.mention} fue señalado por la ruleta.\n"
            "Las miradas pesan más que el castigo."
        )
        gif = "Mor/dislike.gif"

    # 🔴 EXPULSIÓN
    else:
        invite = await canal.create_invite(max_uses=1, unique=True)

        texto = f"💀 {usuario.mention} fue **expulsado del servidor** por decisión de la ruleta."
        gif = "Mor/castigo.gif"

        # 📢 ANUNCIO EN EL SERVIDOR (ANTES DEL KICK)
        embed_final = discord.Embed(
            title="⚖️ Castigo Ejecutado",
            description=texto,
            color=discord.Color.dark_red()
        )
        embed_final.set_image(url="attachment://castigo.gif")

        await canal.send(
            content=usuario.mention,
            embed=embed_final,
            file=discord.File(gif, filename="castigo.gif")
        )

        # 📩 MD
        try:
            await usuario.send(
                "💀 Has sido expulsado por decisión de la ruleta.\n"
                f"🔗 Regresa si te atreves: {invite}"
            )
        except:
            pass

        # 💀 KICK FINAL
        await guild.kick(usuario, reason="Castigo decidido por la ruleta")
        return  # ✅ Aquí solo return, sin paréntesis extra

    # ✨ Enviar embed para silencio o avergonzar
    embed_final = discord.Embed(
        title="⚖️ Castigo Decidido",
        description=texto,
        color=discord.Color.orange() if castigo == "avergonzar" else discord.Color.green()
    )
    embed_final.set_image(url=f"attachment://{os.path.basename(gif)}")

    await canal.send(
        content=usuario.mention,
        embed=embed_final,
        file=discord.File(gif, filename=os.path.basename(gif))
    )

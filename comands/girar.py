import discord
from discord import app_commands
import random
import asyncio

EMOJI_RANDOM = "<a:random:1451014515473911828>"
ID_MOR = 903114752060977202  # tu ID

@app_commands.command(name="girar", description="Gira la ruleta")
async def girar(interaction: discord.Interaction):
    jugadores = interaction.client.jugadores

    if not jugadores:
        await interaction.response.send_message(
            "❌ No hay jugadores en la ruleta.",
            ephemeral=True
        )
        return

    # 🎰 EMBED DE RUEDA GIRANDO
    embed_ruleta = discord.Embed(
        title="🎰 Girando la ruleta...",
        description=(
            f"{EMOJI_RANDOM} Las probabilidades se retuercen...\n"
            "¿Quién será el elegido esta vez?"
        ),
        color=discord.Color.red()
    )
    embed_ruleta.set_image(url="attachment://ruleta.gif")

    await interaction.response.send_message(
        embed=embed_ruleta,
        file=discord.File("Mor/ruleta.gif", filename="ruleta.gif")
    )

    mensaje_ruleta = await interaction.original_response()

    # ⏳ DRAMA
    await asyncio.sleep(4)

    # 🗑️ BORRAR ANIMACIÓN
    await mensaje_ruleta.delete()

    # 🎯 ELEGIR JUGADOR
    elegido = random.choice(jugadores)

    # ✨ TEXTO SEGÚN QUIÉN SEA
    if elegido.id == ID_MOR:
        descripcion = (
            "💫 **Oh… qué coincidencia tan deliciosa.**\n\n"
            "La ruleta se inclinó por pura voluntad del caos.\n"
            f"👑 **{elegido.mention}** ha sido elegida."
        )
    else:
        descripcion = (
            "🎯 La suerte ya decidió.\n\n"
            "Sin escapatoria, sin excusas.\n"
            f"✨ **{elegido.mention}**, la ruleta te reclama."
        )

    # 📢 EMBED FINAL
    embed_resultado = discord.Embed(
        title="🎉 Resultado de la Ruleta",
        description=descripcion,
        color=discord.Color.red()
    )
    embed_resultado.set_image(url="attachment://anuncio.gif")

    await interaction.followup.send(
        embed=embed_resultado,
        file=discord.File("Mor/anuncio.gif", filename="anuncio.gif")
    )

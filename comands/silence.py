import discord
from discord import app_commands

OWNER_ID = 903114752060977202

@app_commands.command(name="silence", description="Activar o desactivar el silencio absoluto")
@app_commands.describe(modo="on o off")
async def silence(interaction: discord.Interaction, modo: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ No tienes autoridad para usar esto.",
            ephemeral=True
        )
        return

    bot = interaction.client
    modo = modo.lower()

    if modo == "on":
        bot.silence_mode = True
        mensaje = "🔇 **Silencio activado.** Solo Mor puede hablar ahora."
    elif modo == "off":
        bot.silence_mode = False
        mensaje = "🔊 **Silencio desactivado.** El caos puede continuar."
    else:
        await interaction.response.send_message(
            "⚠️ Usa `on` o `off`.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="⚠️ Control Absoluto",
        description=mensaje,
        color=discord.Color.dark_red()
    )

    await interaction.response.send_message(embed=embed)

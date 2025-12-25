import discord
from discord import app_commands

EMOJI_ENOJO = "<:enojo:1451014466547220561>"

@app_commands.command(name="end", description="Finaliza la ruleta")
async def end(interaction: discord.Interaction):
    bot = interaction.client
    guild = interaction.guild
    rol = discord.utils.get(guild.roles, name="Ruleta")

    for j in bot.jugadores:
        await j.remove_roles(rol)

    bot.jugadores.clear()

    await interaction.response.send_message(
        f"{EMOJI_ENOJO} La ruleta ha terminado."
    )

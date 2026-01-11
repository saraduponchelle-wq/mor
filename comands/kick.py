import discord
from discord import app_commands

NOMBRE_ROL = "Ruleta"
CANAL_RULETA_ID = 1447699143417135145

EMOJI_ENOJO = "<:enojo:1451014466547220561>"

@app_commands.command(name="kick", description="expulsar jugador de la ruleta")
@app_commands.describe(usuario="expulsar jugador de la ruleta")
async def kick(interaction: discord.Interaction, usuario: discord.Member):
    bot = interaction.client
    guild = interaction.guild

    # ❌ No hay ruleta activa
    if not bot.mensaje_registro:
        await interaction.response.send_message(
            "❌ No hay un ruleta activa ahora",
            ephemeral=True
        )
        return

    # ❌ No está en la ruleta
    if usuario not in bot.jugadores:
        await interaction.response.send_message(
            "❌ El usuario no esta en la ruleta",
            ephemeral=True
        )
        return

    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    # Quitar jugador
    bot.jugadores.remove(usuario)
    if rol:
        await usuario.remove_roles(rol)

    await interaction.response.send_message(
        f"{EMOJI_ENOJO} {usuario.mention} a sido expulsado de la ruleta."
    )

    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        await canal.send(
            f"{EMOJI_ENOJO} {usuario.mention} bye bye"
        )

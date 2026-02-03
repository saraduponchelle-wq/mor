import discord
from discord import app_commands

CANAL_CONFESIONES = 123456789012345678  # cambia esto

@app_commands.command(name="confesion", description="Envía una confesión anónima 💌")
@app_commands.describe(
    usuario="¿Para quién es la confesión?",
    mensaje="Tu confesión",
    revelar_nombre="¿Quieres mostrar tu nombre?"
)
async def confesion(
    interaction: discord.Interaction,
    usuario: discord.Member,
    mensaje: str,
    revelar_nombre: bool
):
    embed = discord.Embed(
        title="💖 Confesión Anónima",
        description=mensaje,
        color=discord.Color.pink()
    )

    embed.add_field(
        name="Para",
        value=usuario.mention,
        inline=False
    )

    if revelar_nombre:
        embed.set_footer(text=f"De: {interaction.user}")
    else:
        embed.set_footer(text="De: Anónimo")

    canal = interaction.guild.get_channel(CANAL_CONFESIONES)
    await canal.send(embed=embed)

    await interaction.response.send_message(
        "💌 Tu confesión fue enviada",
        ephemeral=True
    )

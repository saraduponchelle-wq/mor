import discord
from discord import app_commands

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

@app_commands.command(name="help", description="Lista de comandos")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"{EMOJI_RANDOM} Comandos disponibles",
        description=f"{EMOJI_JIJI} Todos obedecen a mi creadora 👑",
        color=discord.Color.purple()
    )

    for cmd in interaction.client.tree.get_commands():
        embed.add_field(
            name=f"/{cmd.name}",
            value=cmd.description or "Sin descripción",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)

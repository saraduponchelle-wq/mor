import discord
import random
import os
from discord import app_commands

CANAL_YES = 1468127065168416820
CANAL_NO = 1468127204465578136

YES_PATH = "images/yes"
NO_PATH = "images/no"

class InvitacionView(discord.ui.View):
    def __init__(self, bot, guild_id, autor, invitado):
        super().__init__(timeout=86400)
        self.bot = bot
        self.guild_id = guild_id
        self.autor = autor
        self.invitado = invitado

    def get_guild(self):
        return self.bot.get_guild(self.guild_id)

    @discord.ui.button(label="💖 Aceptar", style=discord.ButtonStyle.success)
    async def aceptar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.invitado.id:
            return

        guild = self.get_guild()
        canal = guild.get_channel(CANAL_YES)

        img = random.choice(os.listdir(YES_PATH))

        await canal.send(
            f"💘 **{self.autor.mention} y {self.invitado.mention} pasarán juntos el 14 de febrero**",
            file=discord.File(f"{YES_PATH}/{img}")
        )

        await interaction.response.send_message("💖 Aceptaste la invitación", ephemeral=True)
        self.stop()

    @discord.ui.button(label="💔 Rechazar", style=discord.ButtonStyle.danger)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.invitado.id:
            return

        guild = self.get_guild()
        canal = guild.get_channel(CANAL_NO)

        img = random.choice(os.listdir(NO_PATH))

        embed = discord.Embed(
            title="💔 Rechazo amoroso",
            description=f"{self.autor.mention} fue rechazado",
            color=discord.Color.red()
        )

        await canal.send(
            embed=embed,
            file=discord.File(f"{NO_PATH}/{img}")
        )

        await interaction.response.send_message("💔 Rechazaste la invitación", ephemeral=True)
        self.stop()


@app_commands.command(
    name="sanvalentin",
    description="Invita a alguien a ser tu San Valentín 💘"
)
async def sanvalentin(interaction: discord.Interaction, usuario: discord.Member):
    view = InvitacionView(
        bot=interaction.client,
        guild_id=interaction.guild.id,
        autor=interaction.user,
        invitado=usuario
    )

    await usuario.send(
        f"💌 **{interaction.user} quiere ser tu San Valentín**",
        view=view
    )

    await interaction.response.send_message(
        "💘 Invitación enviada por privado",
        ephemeral=True
    )
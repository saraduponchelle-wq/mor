from discord.ext import commands
import discord
from cogs.menu import enviar_menu

class MenuBar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menubar(self, ctx, balance: int = None):
        await enviar_menu(
            ctx,
            menu_file="menus/bar.json",
            titulo="🍸 Carta del Bar",
            color=discord.Color.dark_red(),
            balance=balance
        )

async def setup(bot):
    await bot.add_cog(MenuBar(bot))

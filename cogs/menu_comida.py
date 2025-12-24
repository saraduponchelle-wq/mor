from discord.ext import commands
import discord
from cogs.menu import enviar_menu

class MenuComida(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menucomida(self, ctx, balance: int = None):
        await enviar_menu(
            ctx,
            menu_file="menus/comida.json",
            titulo="🍽️ Menú de Comida",
            color=discord.Color.orange(),
            balance=balance
        )

async def setup(bot):
    await bot.add_cog(MenuComida(bot))


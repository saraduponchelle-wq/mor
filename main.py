import discord
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # EVENTS
        from events.ready import on_ready
        from events.reaction_add import on_reaction_add
        from events.reaction_remove import on_reaction_remove

        self.add_listener(on_ready)
        self.add_listener(on_reaction_add)
        self.add_listener(on_reaction_remove)

        # ADMIN
        from admin.solo_owner import solo_owner
        self.tree.add_command(solo_owner)

        # COMMANDS
        from commands.start import start
        from commands.end import end
        from commands.girar import girar
        from commands.orden import orden
        from commands.reto import reto
        from commands.adorar import adorar
        from commands.help import help_cmd

        self.tree.add_command(start)
        self.tree.add_command(end)
        self.tree.add_command(girar)
        self.tree.add_command(orden)
        self.tree.add_command(reto)
        self.tree.add_command(adorar)
        self.tree.add_command(help_cmd)

        # MENUS (directos)
        from menus.comida import menucomida
        from menus.bar import menubar

        self.tree.add_command(menucomida)
        self.tree.add_command(menubar)

        await self.tree.sync()

bot = Bot()

bot.jugadores = []
bot.mensaje_registro = None

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

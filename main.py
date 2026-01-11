import discord
from discord import app_commands
from events.reaction_add import handle_reaction_add
from events.reaction_remove import handle_reaction_remove
from database.db import setup_db
import os


# ───────── CONFIG ─────────

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True
INTENTS.reactions = True

# ───────── CLIENTE ─────────

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=INTENTS)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # sincroniza slash commands
        await self.tree.sync()
        print("✅ Slash commands sincronizados")

bot = Bot()

# 🔹 estado global del juego
bot.jugadores = []
bot.mensaje_registro = None
bot.NOMBRE_ROL = "Jugador"
OWNER_ID = 903114752060977202
bot.silence_mode = False



# ───────── EVENTOS ─────────

@bot.event
async def on_ready():
    setup_db()
    print(f"🤖 Bot conectado como {bot.user}")

@bot.event
async def on_member_join(member):
    # ejemplo (opcional)
    print(f"➕ {member} se unió al servidor")

@bot.event
async def on_member_remove(member):
    # ejemplo (opcional)
    print(f"➖ {member} salió del servidor")

# ───────── REACCIONES ─────────
# (esto conecta con tu sistema de registro)


@bot.event
async def on_reaction_add(reaction, user):
    await handle_reaction_add(bot, reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):
    await handle_reaction_remove(bot, reaction, user)


# ───────── IMPORTAR COMANDOS ─────────
# aquí conectas tus archivos externos

# Admin
from comands.start import start
from comands.end import end
from comands.adorar import adorar
from comands.girar import girar
from comands.help import help_cmd
from comands.orden import orden
from comands.reto import reto
from comands.silence import silence
from comands.punition import punition
from comands.kiss import beso
from comands.join import join
from comands.kick import kick
from comands.salonp import salonp_group



# Luego registrarlos en tu bot





# Menús
from menus.menu import menu_group
from comands.salonp import salonp_create, salonp_invite, salonp_eliminate


#silencio
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if bot.silence_mode and interaction.user.id != OWNER_ID:
        if interaction.type == discord.InteractionType.application_command:
            await interaction.response.send_message(
                "🤫 El silencio reina ahora mismo…",
                ephemeral=True
            )
            return
    # await bot.process_application_commands(interaction)






# from menus.bar import mostrar_menu_bar

# ───────── REGISTRAR SLASH COMMANDS ─────────

bot.tree.add_command(adorar)
bot.tree.add_command(menu_group)
bot.tree.add_command(start)
bot.tree.add_command(reto)
bot.tree.add_command(orden)
bot.tree.add_command(girar)
bot.tree.add_command(end)
bot.tree.add_command(help_cmd)
bot.tree.add_command(silence)
bot.tree.add_command(punition)
bot.tree.add_command(beso)
bot.tree.add_command(join)
bot.tree.add_command(kick)


# Registrar

# registrar comandos
bot.tree.add_command(salonp_group)






# ───────── RUN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
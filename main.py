import discord
from discord import app_commands
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

# ───────── EVENTOS ─────────

@bot.event
async def on_ready():
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

jugadores = []
mensaje_registro = None
NOMBRE_ROL = "Jugador"  # cambia si hace falta

@bot.event
async def on_reaction_add(reaction, user):
    global mensaje_registro

    if user.bot or not mensaje_registro:
        return

    if reaction.message.id != mensaje_registro.id:
        return

    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if not rol or member in jugadores:
        return

    jugadores.append(member)
    await member.add_roles(rol)

@bot.event
async def on_reaction_remove(reaction, user):
    global mensaje_registro

    if user.bot or not mensaje_registro:
        return

    if reaction.message.id != mensaje_registro.id:
        return

    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if member in jugadores:
        jugadores.remove(member)
        await member.remove_roles(rol)

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


# Menús
from menus.comida import mostrar_menu_comida

# from menus.bar import mostrar_menu_bar

# ───────── REGISTRAR SLASH COMMANDS ─────────

bot.tree.add_command(start)
bot.tree.add_command(end)

bot.tree.add_command(adorar)
bot.tree.add_command(girar)
bot.tree.add_command(orden)
bot.tree.add_command(reto)
bot.tree.add_command(help_cmd)

# ───────── RUN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
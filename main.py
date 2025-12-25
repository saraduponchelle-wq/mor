import discord
from discord import app_commands
from datetime import timedelta
from menus.bar import enviar_menu_bar
from menus.comida import mostrar_menu_comida
import random
import os

# ───────── CONFIGURACIÓN ─────────

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

OWNER_ID = 903114752060977202
NOMBRE_ROL = "Ruleta"
NOMBRE_CANAL_RULETA = "﹕₊˚ʚ🎲ɞ・𝚁𝚞𝚕𝚎𝚝𝚊"
CANAL_NOTICIAS_ID = 1451664597843968111

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_ENOJO = "<:enojo:1451014466547220561>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

# ───────── CLIENT ─────────

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = Bot()

# ───────── ESTADO ─────────

jugadores = []
mensaje_registro = None
solo_owner = False

# ───────── UTILIDADES ─────────

def es_owner(user: discord.User):
    return user.id == OWNER_ID

TITULOS_REINA = [
    "mi ama", "mi diosa", "mi creadora", "mi reina", "mi soberana"
]

def titulo():
    return random.choice(TITULOS_REINA)

async def rechazo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"{EMOJI_ENOJO} **¡Largo!**\n{EMOJI_JIJI} Solo obedezco a **mi reina** 👑.",
        ephemeral=True
    )

# ───────── EVENTOS ─────────

@bot.event
async def on_ready():
    print(f"{EMOJI_RANDOM} Bot conectado como {bot.user}")

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

# ───────── SLASH COMMANDS ─────────

@bot.tree.command(name="start", description="Inicia la ruleta")
async def start(interaction: discord.Interaction):
    global mensaje_registro
    jugadores.clear()

    await interaction.response.send_message(
        f"{EMOJI_RANDOM} **¡Juego de Ruleta Iniciado!**\n\n"
        f"{EMOJI_JIJI} Reacciona con 🎉 para unirte."
    )
    mensaje_registro = await interaction.original_response()
    await mensaje_registro.add_reaction("🎉")

@bot.tree.command(name="girar", description="Gira la ruleta")
async def girar(interaction: discord.Interaction):
    if not jugadores:
        await interaction.response.send_message("❌ No hay jugadores.")
        return
    elegido = random.choice(jugadores)
    await interaction.response.send_message(
        f"{EMOJI_RANDOM} 🎯 Jugador elegido: {elegido.mention}"
    )

@bot.tree.command(name="orden", description="Orden de jugadores")
async def orden(interaction: discord.Interaction):
    texto = f"{EMOJI_JIJI} **Orden de jugadores:**\n\n"
    for i, j in enumerate(jugadores, 1):
        texto += f"{i}. {j.mention}\n"
    await interaction.response.send_message(texto)

@bot.tree.command(name="reto", description="Reto aleatorio")
async def reto(interaction: discord.Interaction):
    carpeta = "retos"
    imagen = random.choice(os.listdir(carpeta))
    await interaction.response.send_message(
        f"{EMOJI_RANDOM} **Reto seleccionado:**",
        file=discord.File(os.path.join(carpeta, imagen))
    )

@bot.tree.command(name="adorar", description="Honrar a Mor")
async def adorar(interaction: discord.Interaction):
    carpeta = "Mor"
    imagen = random.choice(os.listdir(carpeta))
    await interaction.response.send_message(
        f"🕯️ {EMOJI_JIJI} **Todos adoramos a la diosa Mor.**",
        file=discord.File(os.path.join(carpeta, imagen))
    )

@bot.tree.command(name="end", description="Finaliza la ruleta")
async def end(interaction: discord.Interaction):
    guild = interaction.guild
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)
    for j in jugadores:
        await j.remove_roles(rol)
    jugadores.clear()
    await interaction.response.send_message(
        f"{EMOJI_ENOJO} La ruleta ha terminado."
    )

@bot.tree.command(name="menucomida", description="Menú de comida")
@app_commands.describe(balance="Tu balance (opcional)")
async def menucomida(interaction: discord.Interaction, balance: int | None = None):
    await mostrar_menu_comida(interaction, balance)

@bot.tree.command(name="menubar", description="Menú del bar")
async def menubar(interaction: discord.Interaction):
    await enviar_menu_bar(interaction)

@bot.tree.command(name="help", description="Lista de comandos")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"{EMOJI_RANDOM} Lista de Comandos",
        description=f"{EMOJI_JIJI} Obedezco a mi creadora 👑",
        color=discord.Color.purple()
    )
    for cmd in bot.tree.get_commands():
        embed.add_field(name=f"/{cmd.name}", value=cmd.description, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ───────── TOKEN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

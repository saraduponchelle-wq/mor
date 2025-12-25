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
CANAL_RULETA_ID = 1447699143417135145
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

    # 🔽🔽🔽 ESTO ES LO NUEVO 🔽🔽🔽
    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(
                f"👑✨ {EMOJI_JIJI} **Mi creadora ha descendido a la ruleta.**\n"
                f"{EMOJI_RANDOM} El destino se inclina ante ti."
            )
        else:
            await canal.send(
                f"{EMOJI_RANDOM} {member.mention} se unió a la ruleta."
            )


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

    if member not in jugadores:
        return

    jugadores.remove(member)
    await member.remove_roles(rol)

    # 🔽🔽🔽 ESTO ES LO QUE FALTABA 🔽🔽🔽
    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(
                f"🕯️👑 {EMOJI_JIJI} **Mi creadora ha abandonado la ruleta.**"
            )
        else:
            await canal.send(
                f"{EMOJI_ENOJO} {member.mention} salió de la ruleta."
            )


# ───────── SLASH COMMANDS ─────────

@bot.tree.command(name="start", description="Inicia la ruleta")
async def start(interaction: discord.Interaction):
    global mensaje_registro
    jugadores.clear()

    # Mensaje principal con reacción
    await interaction.response.send_message(
        f"{EMOJI_RANDOM} **¡Juego de Ruleta Iniciado!**\n\n"
        f"{EMOJI_JIJI} Reacciona con 🎉 para unirte."
    )

    mensaje_registro = await interaction.original_response()
    await mensaje_registro.add_reaction("🎉")

    guild = interaction.guild
    canal_noticias = guild.get_channel(CANAL_NOTICIAS_ID)

    # Aviso público
    if canal_noticias:
        await canal_noticias.send(
            f"@everyone {EMOJI_RANDOM} **¡La ruleta ha comenzado!**\n"
            f"{EMOJI_JIJI} Ve al canal del juego."
        )

    # Evento programado (igual que antes)
    inicio = discord.utils.utcnow() + timedelta(minutes=1)
    fin = inicio + timedelta(hours=1)

    try:
        await guild.create_scheduled_event(
            name="🎰 Ruleta en marcha",
            description="La ruleta ha comenzado.\nReacciona para participar.",
            start_time=inicio,
            end_time=fin,
            entity_type=discord.EntityType.external,
            location="Ruleta del servidor",
            privacy_level=discord.PrivacyLevel.guild_only
        )
    except Exception as e:
        print("Error creando evento:", e)


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

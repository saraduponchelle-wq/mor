import discord
from discord.ext import commands
from datetime import timedelta
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
CANAL_NOTICIAS_ID = 1448855806232494130

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_ENOJO = "<:enojo:1451014466547220561>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command=None
)

# ───────── ESTADO ─────────

jugadores = []
mensaje_registro = None
solo_owner = False

# ───────── UTILIDADES ─────────

def es_owner(ctx):
    return ctx.author.id == OWNER_ID

TITULOS_REINA = [
    "mi ama",
    "mi diosa",
    "mi creadora",
    "mi reina",
    "mi soberana"
]

def titulo():
    return random.choice(TITULOS_REINA)

async def rechazo(ctx):
    await ctx.send(
        f"{EMOJI_ENOJO} **¡Largo!**\n"
        f"{EMOJI_JIJI} Solo obedezco a **mi reina** 👑."
    )

@bot.check
async def bloqueo_global(ctx):
    if solo_owner and ctx.author.id != OWNER_ID:
        await ctx.send(f"{EMOJI_ENOJO} Silencio. No eres mi creadora.")
        return False
    return True

# ───────── EVENTOS ─────────

@bot.event
async def on_ready():
    print(f"{EMOJI_RANDOM} Bot conectado como {bot.user}")

# ───────── START ─────────

@bot.command()
async def start(ctx):
    global mensaje_registro
    jugadores.clear()

    mensaje_registro = await ctx.send(
        f"{EMOJI_RANDOM} **¡Juego de Ruleta Iniciado!**\n\n"
        f"{EMOJI_JIJI} Reacciona con 🎉 para unirte."
    )
    await mensaje_registro.add_reaction("🎉")

    guild = ctx.guild
    canal_noticias = guild.get_channel(CANAL_NOTICIAS_ID)

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

        if canal_noticias:
            await canal_noticias.send(
                f"@everyone {EMOJI_RANDOM} **¡La ruleta ha comenzado!**\n"
                f"{EMOJI_JIJI} Ve al canal del juego."
            )
    except Exception as e:
        print("Error creando evento:", e)

    await ctx.send(f"{EMOJI_JIJI} La ruleta está abierta.")

# ───────── REACCIONES ─────────

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

    canal = discord.utils.get(guild.text_channels, name=NOMBRE_CANAL_RULETA)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(
                f"👑✨ {EMOJI_JIJI} **Mi creadora ha descendido a la ruleta.**\n"
                f"{EMOJI_RANDOM} El destino se inclina ante ti."
            )
        else:
            await canal.send(f"{EMOJI_RANDOM} {member.mention} se unió a la ruleta.")

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

    canal = discord.utils.get(guild.text_channels, name=NOMBRE_CANAL_RULETA)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(
                f"🕯️👑 {EMOJI_JIJI} **Mi creadora ha abandonado la ruleta.**"
            )
        else:
            await canal.send(f"{EMOJI_ENOJO} {member.mention} salió de la ruleta.")

# ───────── COMANDOS ─────────

@bot.command()
async def girar(ctx):
    if not jugadores:
        await ctx.send("❌ No hay jugadores.")
        return
    elegido = random.choice(jugadores)
    await ctx.send(f"{EMOJI_RANDOM} 🎯 Jugador elegido: {elegido.mention}")

@bot.command()
async def orden(ctx):
    if not jugadores:
        await ctx.send("❌ No hay jugadores.")
        return
    texto = f"{EMOJI_JIJI} **Orden de jugadores:**\n\n"
    for i, j in enumerate(jugadores, 1):
        texto += f"{i}. {j.mention}\n"
    await ctx.send(texto)

@bot.command()
async def reto(ctx):
    carpeta = "retos"
    if not os.path.exists(carpeta):
        await ctx.send("❌ No hay retos.")
        return
    imagen = random.choice(os.listdir(carpeta))
    ruta = os.path.join(carpeta, imagen)

    if ctx.author.id == OWNER_ID:
        await ctx.send(
            f"🕯️👑 {EMOJI_JIJI} Un reto digno de mi diosa.",
            file=discord.File(ruta)
        )
    else:
        await ctx.send(
            f"{EMOJI_RANDOM} **Reto seleccionado:**",
            file=discord.File(ruta)
        )

@bot.command()
async def adorar(ctx):
    carpeta = "Mor"
    imagen = random.choice(os.listdir(carpeta))
    await ctx.send(
        f"🕯️ {EMOJI_JIJI} **Todos adoramos a la diosa Mor.**",
        file=discord.File(os.path.join(carpeta, imagen))
    )

@bot.command()
async def end(ctx):
    guild = ctx.guild
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)
    for j in jugadores:
        await j.remove_roles(rol)
    jugadores.clear()
    await ctx.send(f"{EMOJI_ENOJO} La ruleta ha terminado.")

# ───────── HELP ─────────

@bot.command(name="help")
async def ayuda(ctx):
    embed = discord.Embed(
        title=f"{EMOJI_RANDOM} Lista de Comandos",
        description=f"{EMOJI_JIJI} Obedezco a mi creadora 👑",
        color=discord.Color.purple()
    )

    embed.add_field(name=".start", value="Inicia la ruleta", inline=False)
    embed.add_field(name=".girar", value="Gira la ruleta", inline=False)
    embed.add_field(name=".orden", value="Orden de jugadores", inline=False)
    embed.add_field(name=".reto", value="Reto aleatorio", inline=False)
    embed.add_field(name=".adorar", value="Honrar a Mor", inline=False)
    embed.add_field(name=".end", value="Finaliza el juego", inline=False)

    if es_owner(ctx):
        embed.add_field(
            name="👑 Comandos de mi Reina",
            value=(
                "• .banner\n"
                "• .pfp\n"
                "• .desc\n"
                "• .castigar\n"
                "• .perdonar\n"
            ),
            inline=False
        )

    await ctx.send(embed=embed)

TITULOS_REINA = [
    "mi ama",
    "mi diosa",
    "mi creadora",
    "mi reina",
    "mi soberana"
]

def titulo():
    return random.choice(TITULOS_REINA)

async def rechazo(ctx):
    await ctx.send("🚫 **¡Largo!** Tú no eres mi hermosa creadora. Solo obedezco a **mi reina** 👑.")

@bot.command()
async def banner(ctx):
    if not es_owner(ctx):
        await rechazo(ctx)
        return

    ruta = None
    for ext in (".png", ".jpg"):
        posible = f"images/banner{ext}"
        if os.path.exists(posible):
            ruta = posible
            break


    if not os.path.exists(ruta):
        await ctx.send(f"😔 Lo siento, {titulo()}, no encontré el banner en **images/banner.png**.")
        return

    with open(ruta, "rb") as f:
        await bot.user.edit(banner=f.read())

    await ctx.send(f"🖼️ El estandarte ha sido cambiado como ordenaste, {titulo()} 👑")

@bot.command()
async def pfp(ctx):
    if not es_owner(ctx):
        await rechazo(ctx)
        return

    ruta = None
    for ext in (".png", ".jpg"):
        posible = f"images/pfp{ext}"
        if os.path.exists(posible):
            ruta = posible
            break


    if not os.path.exists(ruta):
        await ctx.send(f"😔 Perdóname, {titulo()}, no hallé la imagen de perfil.")
        return

    with open(ruta, "rb") as f:
        await bot.user.edit(avatar=f.read())

    await ctx.send(f"👤 He adoptado una nueva apariencia para complacerte, {titulo()} ✨")

@bot.command()
async def desc(ctx, *, texto: str):
    if not es_owner(ctx):
        await rechazo(ctx)
        return

    await bot.change_presence(
        activity=discord.CustomActivity(name=texto)
    )
    await ctx.send(f"✏️ Mi esencia ha sido reescrita según tu voluntad, {titulo()} 🕯️")

@bot.command()
async def silencio(ctx, estado: str):
    global solo_owner

    if not es_owner(ctx):
        await ctx.send("🚫 Largo. Solo obedezco a **mi creadora**.")
        return

    if estado.lower() == "on":
        solo_owner = True
        await ctx.send("🔇 Solo escucharé la voz de **mi reina**.")
    elif estado.lower() == "off":
        solo_owner = False
        await ctx.send("🔊 Vuelvo a escuchar a los mortales.")
    else:
        await ctx.send("❓ Usa `.silencio on` o `.silencio off`")

@bot.command()
async def castigar(ctx, miembro: discord.Member):
    if not es_owner(ctx):
        await ctx.send("🔥 Largo. Solo mi diosa puede castigar.")
        return

    if miembro.top_role >= ctx.guild.me.top_role:
        await ctx.send(
            "⚠️ Mi reina… ese ser está por encima de mi autoridad."
        )
        return

    overwrite = ctx.channel.overwrites_for(miembro)
    overwrite.send_messages = False

    try:
        await ctx.channel.set_permissions(miembro, overwrite=overwrite)
        await ctx.send(
            f"⚔️ {miembro.mention} ha sido silenciado por orden de **mi reina**."
        )
    except discord.Forbidden:
        await ctx.send(
            "❌ No tengo permisos suficientes para ejecutar tu voluntad."
        )


@bot.command()
async def perdonar(ctx, miembro: discord.Member):
    if not es_owner(ctx):
        await ctx.send("❌ No tienes autoridad para perdonar.")
        return

    overwrite = ctx.channel.overwrites_for(miembro)
    overwrite.send_messages = None
    await ctx.channel.set_permissions(miembro, overwrite=overwrite)

    await ctx.send(
        f"🕊️ {miembro.mention} ha sido perdonado por **mi ama**."
    )

@bot.command()
async def embed(ctx):
    embed = discord.Embed(
        title="🎄 ¡Evento Navideño Iniciado! 🎄\n",
        description=(
            "La magia de la Navidad llega al servidor ✨\n"
            "Da inicio nuestra **gran rifa navideña**, auspiciada por **Mor**.\n"
        ),
        color=discord.Color.red()
    )

    embed.add_field(
        name="🎁 Premios de la rifa",
        value=(
            "🥇 **Primer lugar:** 1 mes de Discord Nitro + rol especial exclusivo\n"
            "🥈 **Segundo lugar:** Marco de la tienda + rol especial\n"
            "🥉 **Tercer lugar:** Rol especial\n"
        ),
        inline=False
    )

    embed.add_field(
        name="💰 ¿Cómo participar?",
        value=(
            "Consigue **2000 monedas** usando el nuevo bot de economía.\n"
            "Las monedas se obtienen **hablando en los chats del servidor**.\n"
            "*No cuentan los chats de bots.*\n"
        ),
        inline=False
    )

    embed.add_field(
        name="🛒 Compra del ticket",
        value="Compra el ticket usando el comando:\n`/item store`\n",
        inline=False
    )

    embed.add_field(
        name="🎯 Monedas extra",
        value=(
            "• Retos especiales los fines de semana\n"
            "• Pequeños juegos que otorgan monedas\n"
        ),
        inline=False
    )

    embed.add_field(
        name="📅 Fecha del sorteo",
        value="🗓️ **Martes 23 en la mañana**\n",
        inline=False
    )

    embed.set_footer(text="🎅 Evento navideño • Auspiciado por Mor")

    await ctx.send(
        content="@everyone 🎉 ¡No se pierdan el evento!",
        embed=embed
    )


# ───────── TOKEN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

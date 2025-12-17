import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(
    command_prefix='.',
    intents=intents,
    help_command=None
)



jugadores = []
mensaje_registro = None
NOMBRE_ROL = "Ruleta"


# -------------------------
#  Evento: Bot Listo
# -------------------------
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# -------------------------
#  COMANDO: Iniciar juego
# -------------------------
@bot.command()
async def start(ctx):
    global mensaje_registro
    jugadores.clear()

    mensaje_registro = await ctx.send(
        "🎰 **¡Juego de Ruleta Iniciado!**\n\n"
        "Reacciona con 🎉 para unirte al juego."
    )

    await mensaje_registro.add_reaction("🎉")
    await ctx.send("Los jugadores pueden empezar a reaccionar.")

# -------------------------
#  Evento: Reacciones
# -------------------------
@bot.event
async def on_reaction_add(reaction, user):
    global mensaje_registro

    if user.bot:
        return

    if mensaje_registro is None or reaction.message.id != mensaje_registro.id:
        return

    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if rol is None:
        return

    if member not in jugadores:
        jugadores.append(member)
        await member.add_roles(rol)
        await reaction.message.channel.send(
            f"➡️ {member.mention} se ha unido a la ruleta 🎰"
        )


@bot.event
async def on_reaction_remove(reaction, user):
    global mensaje_registro

    if user.bot:
        return

    if mensaje_registro is None or reaction.message.id != mensaje_registro.id:
        return

    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if rol is None:
        return

    if member in jugadores:
        jugadores.remove(member)
        await member.remove_roles(rol)
        await reaction.message.channel.send(
            f"⬅️ {member.mention} salió de la ruleta"
        )


# -------------------------
#  COMANDO: Elegir jugador al azar
# -------------------------
@bot.command()
async def randomplayer(ctx):
    if not jugadores:
        await ctx.send("❌ No hay jugadores registrados.")
        return

    elegido = random.choice(jugadores)
    await ctx.send(f"🎯 Jugador seleccionado: {elegido.mention}")

# -------------------------
#  COMANDO: Elegir reto (imagen al azar)
# -------------------------
@bot.command()
async def reto(ctx):
    carpeta = "retos"  # Carpeta donde guardas tus imágenes

    if not os.path.exists(carpeta):
        await ctx.send("❌ No existe la carpeta **retos**.")
        return

    imagenes = [f for f in os.listdir(carpeta) if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

    if not imagenes:
        await ctx.send("❌ No hay imágenes en la carpeta **retos**.")
        return

    imagen_elegida = random.choice(imagenes)
    ruta = os.path.join(carpeta, imagen_elegida)

    await ctx.send(
        "🎲 **Reto aleatorio seleccionado:**",
        file=discord.File(ruta)
    )

# -------------------------
#  COMANDO: Terminar juego
# -------------------------
@bot.command()
async def end(ctx):
    guild = ctx.guild
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    for miembro in jugadores:
        if rol in miembro.roles:
            await miembro.remove_roles(rol)

    jugadores.clear()
    await ctx.send("🛑 El juego ha sido finalizado y los roles fueron removidos.")
    
# -------------------------
#  COMANDO: Ayuda personalizada
# -------------------------
@bot.command(name="help")
async def ayuda(ctx):
    embed = discord.Embed(
        title="📘 Lista de Comandos",
        color=discord.Color.blue()
    )

    embed.add_field(name=".start", value="Inicia la ruleta y permite unirse con 🎉.", inline=False)
    embed.add_field(name=".girar", value="Gira la ruleta y elige un jugador al azar.", inline=False)
    embed.add_field(name=".orden", value="Muestra el orden actual de los jugadores.", inline=False)
    embed.add_field(name=".reto", value="Selecciona una imagen de reto al azar.", inline=False)
    embed.add_field(name=".adorar", value="Honra a la diosa Mor con una imagen.", inline=False)
    embed.add_field(name=".end", value="Finaliza el juego y limpia los jugadores.", inline=False)



    await ctx.send(embed=embed)

@bot.command()
async def orden(ctx):
    if not jugadores:
        await ctx.send("❌ No hay jugadores en la ruleta.")
        return

    texto = "📜 **Orden de jugadores:**\n\n"
    for i, jugador in enumerate(jugadores, start=1):
        texto += f"{i}. {jugador.mention}\n"

    await ctx.send(texto)

@bot.command()
async def adorar(ctx):
    carpeta = "Mor"

    if not os.path.exists(carpeta):
        await ctx.send("❌ No existe la carpeta **Mor**.")
        return

    imagenes = [f for f in os.listdir(carpeta)
                if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

    if not imagenes:
        await ctx.send("❌ No hay imágenes en la carpeta **Mor**.")
        return

    imagen = random.choice(imagenes)
    ruta = os.path.join(carpeta, imagen)

    await ctx.send(
        "🕯️ **Todos adoramos a la diosa Mor. En paz descanse.**",
        file=discord.File(ruta)
    )


# -------------------------
#  INICIAR BOT
# -------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

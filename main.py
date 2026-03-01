import discord
from discord import app_commands
from events.reaction_add import handle_reaction_add
from events.reaction_remove import handle_reaction_remove
from database.db import setup_db
import os

EMOJI_ELY = str(os.getenv("ELY"))
EMOJI_FLOWER = str(os.getenv("FLOWER"))
EMOJI_SEPARATOR = str(os.getenv("SEPARATOR"))
EMOJI_CIRCLE = str(os.getenv("CIRCLE"))


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
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Feliz San Valentin💘"
        ),
        status=discord.Status.online
    )
    print(f"🤖 Bot conectado como {bot.user}")



BIENVENIDA_CHANNEL_ID = 1447703622501793842
REGLAS_CHANNEL_ID = 1447704211927335016
ROLES_CHANNEL_ID = 1449194573493702726
GENERAL_CHANNEL_ID = 1447695182693798042
SOPORTE_CHANNEL_ID = 1447716741458296962


@bot.event
async def on_member_join(member: discord.Member):

    channel = member.guild.get_channel(BIENVENIDA_CHANNEL_ID)
    if channel is None:
        return

    # 🔹 Obtener menciones reales de canales
    reglas = f"<#{REGLAS_CHANNEL_ID}>"
    roles = f"<#{ROLES_CHANNEL_ID}>"
    general = f"<#{GENERAL_CHANNEL_ID}>"
    soporte = f"<#{SOPORTE_CHANNEL_ID}>"

    # 🔹 Mensaje principal
    mensaje = (
        f"# {EMOJI_FLOWER} Bienvenido a Irelia Palace {EMOJI_FLOWER}\n"
        f"{EMOJI_ELY} Estamos **felices** de tenerte entre nosotros, {member.mention}\n\n"
        f"{EMOJI_ELY} **Antes de comenzar, te invitamos a leer nuestras reglas** en {reglas}\n"
        f"{EMOJI_ELY} **¿Tienes alguna duda?** Si no encuentras la respuesta, el equipo estará encantado de asistirte en {soporte}\n"
        f"{EMOJI_ELY} **Pasa a saludarnos en {general},** nos encanta dar la bienvenida a nuestros nuevos miembros.\n"
        f"{EMOJI_ELY} **Si deseas personalizar tu experiencia,** no olvides obtener tus roles en {roles}"
    )

    # 🔹 Crear embed
    embed = discord.Embed(
        title=f"# {EMOJI_SEPARATOR} • Una nueva historia comienza! ",
        description=(
            "Que la diosa **Mor** te bendiga y haga de tu viaje dentro de "
            "**Irelia Palace** un sueño inolvidable."
        ),
        color=discord.Color.pink()
    )

    # 🔹 Icono del usuario arriba a la derecha
    embed.set_thumbnail(url=member.display_avatar.url)

    # 🔹 Footer opcional elegante
    embed.set_footer(text="Bienvenido a Irelia Palace")

    await channel.send(mensaje, embed=embed)


# @bot.event
# async def on_member_remove(member):
#     # ejemplo (opcional)
#     print(f"➖ {member} salió del servidor")

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
# from comands.start import start
# from comands.end import end
# from comands.adorar import adorar
# from comands.girar import girar
# from comands.help import help_cmd
# from comands.orden import orden
# from comands.reto import reto
# from comands.silence import silence
# from comands.punition import punition
# from comands.kiss import beso
# from comands.join import join
# from comands.kick import kick
# from comands.salonp.salonp_commands import salonp_group
# from comands.embed import evento_amor
# from comands.sanvalentin.confesion import confesion
# from comands.sanvalentin.invitar import sanvalentin



# Luego registrarlos en tu bot


# Menús
from menus.menu import menu_group


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

# bot.tree.add_command(adorar)
# bot.tree.add_command(menu_group)
# bot.tree.add_command(start)
# bot.tree.add_command(reto)
# bot.tree.add_command(orden)
# bot.tree.add_command(girar)
# bot.tree.add_command(end)
# bot.tree.add_command(help_cmd)
# bot.tree.add_command(silence)
# bot.tree.add_command(punition)
# bot.tree.add_command(beso)
# bot.tree.add_command(join)
# bot.tree.add_command(kick)
# bot.tree.add_command(salonp_group)
# bot.tree.add_command(evento_amor)
# bot.tree.add_command(confesion)
# bot.tree.add_command(sanvalentin)


# Registrar

# registrar comandos







# ───────── RUN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN:", TOKEN)
bot.run(TOKEN)
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
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Feliz San Valentin💘"
        ),
        status=discord.Status.online
    )
    print(f"🤖 Bot conectado como {bot.user}")


TARGET_USER_ID = 928321840273825812  # ← aquí pondrás el ID de la persona

# @bot.event
# async def on_message(message: discord.Message):
#     # Ignorar mensajes del bot
#     if message.author.bot:
#         return

#     # Si es la persona objetivo
#     if message.author.id == TARGET_USER_ID:
#         try:
#             # Crear el emoji personalizado
#             await message.add_reaction("🫃")

#             await message.reply(
#                 f"{message.author.mention}, está en busca de un novio para tener sexo gay 24/7"
#             )

#         except Exception as e:
#             print(f"Error en sistema amigo: {e}")


WELCOME_CHANNEL_ID = 1447703622501793842

# @bot.event
# async def on_member_join(member: discord.Member):
#     canal = bot.get_channel(WELCOME_CHANNEL_ID)

#     if canal is None:
#         return

#     embed = discord.Embed(
#         title="💖 Bienvenid@ al reino del amor 💖",
#         description=(
#             f"Hi hi {member.mention}~ 🌸✨\n\n"
#             "Nos alegra muchísimo que formes parte de este pequeño universo lleno de juegos, rol y corazones brillantes 💘\n\n"
#             "Antes de comenzar tu aventura, por favor pasa a leer las reglas aquí:\n"
#             "📜 <#1447704211927335016>\n\n"
#             "Que este San Valentín te regale confesiones dulces, matches mágicos "
#             "y momentos inolvidables 💞🌷"
#         ),
#         color=discord.Color.from_rgb(255, 105, 180)
#     )

#     embed.set_footer(text="Con cariño… Mor, la diosa del amor 💘")

#     await canal.send(embed=embed)

#     # Enviar el gif después
#     await canal.send(file=discord.File("images/welcome.gif"))



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
from comands.salonp.salonp_commands import salonp_group
from comands.embed import evento_amor
from comands.sanvalentin.confesion import confesion
from comands.sanvalentin.invitar import sanvalentin



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

bot.tree.add_command(adorar)
# bot.tree.add_command(menu_group)
# bot.tree.add_command(start)
# bot.tree.add_command(reto)
# bot.tree.add_command(orden)
# bot.tree.add_command(girar)
# bot.tree.add_command(end)
# bot.tree.add_command(help_cmd)
# bot.tree.add_command(silence)
bot.tree.add_command(punition)
bot.tree.add_command(beso)
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
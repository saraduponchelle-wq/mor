import discord
from discord import Emoji, app_commands
from events.reaction_add import handle_reaction_add
from events.reaction_remove import handle_reaction_remove
from database.db import setup_db
import os


EMOJI_ELY = str(os.getenv("ELY"))
EMOJI_FLOWER = str(os.getenv("FLOWER"))
EMOJI_SEPARATOR = str(os.getenv("SEPARATOR"))
EMOJI_CIRCLE = str(os.getenv("CIRCLE"))
EMOJI_HEART = str(os.getenv("HEART"))
EMOJI_STAR = str(os.getenv("STAR"))


USUARIOS_OBJETIVO = [
    698919436354322632,
    947743342249246731
]


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

bot.diversion_activo = False

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

# 🔹 boosters   

BOOST_CHANNEL_ID = 123456789012345678  # <-- ID del canal donde se enviará el mensaje


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):

    # Detecta cuando alguien empieza a boostear
    if before.premium_since is None and after.premium_since is not None:

        channel = after.guild.get_channel(BOOST_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title=f"{EMOJI_FLOWER} Un nuevo impulso para Irelia Palace {EMOJI_FLOWER}",
            description=(
                f"(づ๑•ᴗ•๑)づ {after.mention} ¡Muchas gracias por el boost! {EMOJI_HEART}\n\n"
                f"# {EMOJI_HEART} Tus beneficios:\n"
                f"   {EMOJI_ELY} Un rol totalmente personalizado\n"
                f"   {EMOJI_ELY} Ganar 1000 de dinero diario usando collect income.\n"
                f"   {EMOJI_ELY} Mención de @everyone cuando busques rol."
            ),
            color=discord.Color.from_rgb(186, 85, 211)  # morado elegante
        )

        # Avatar del usuario arriba a la derecha
        embed.set_thumbnail(url=after.display_avatar.url)

        embed.set_footer(text="Irelia Palace • La diosa Mor bendice tu apoyo ✨")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)

# ───────── DESPEDIDA ─────────

DESPEDIDAS_CHANNEL_ID = 1459024989360492645  # <-- pon aquí el ID de tu canal de despedidas


@bot.event
async def on_member_remove(member: discord.Member):

    channel = member.guild.get_channel(DESPEDIDAS_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title=f"**{EMOJI_FLOWER} Una despedida en Irelia Palace {EMOJI_FLOWER}**",
        description=(
            f"{member.mention}\n\n"
            f"{EMOJI_ELY} **Gracias** por haber formado parte de **Irelia Palace**.\n"
            f"{EMOJI_ELY}Que la diosa **Mor** ilumine tu camino, dondequiera que continúe tu historia. ✨"
        ),
        color=discord.Color.from_rgb(255, 182, 193)  # rosa suave elegante
    )

    # Avatar del usuario arriba a la derecha
    embed.set_thumbnail(url=member.display_avatar.url)

    # Footer elegante
    embed.set_footer(text="Irelia Palace • Que Mor te acompañe")

    await channel.send(embed=embed)

# ───────── BIENVENIDA ─────────

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
        title=f"**{EMOJI_SEPARATOR} • Una nueva historia comienza!**",
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

#----------------- HACK ------------------------

from events.detect import handle_invite_detection

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # 🔹 detectar invites
    await handle_invite_detection(bot, message)

    palabra_prohibida = "cuck"

    # 🎯 Diversión
    if bot.diversion_activo and message.author.id in USUARIOS_OBJETIVO:
        try:
            await message.add_reaction(":pregnant_man:")
        except:
            pass

    # 🚫 palabra prohibida
    if palabra_prohibida in message.content.lower():
        await message.delete()

        await message.channel.send(
            f"{message.author.mention} esa palabra no está permitida.\n"
            "No ofendas a la diosa Aertith. ✨"
        )
        return

    await bot.process_commands(message)


#----------------- REACCIONES ------------------------

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
from comands.diversion import diversion

bot.tree.add_command(diversion)

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

SOLICITUDES_CHANNEL_ID = 1478120920781557902  # canal donde va el embed
STAFF_CHANNEL_ID = 1478121103330246656        # canal donde llegan solicitudes
INVITE_CHANNEL_ID = 333333333333333333       # canal donde se crea la invitación
TICKET_MESSAGE_ID = 444444444444444444       # ID del mensaje embed creado
FORM_EMOJI = "📝"
APPROVE_EMOJI = "✅"

# ───────── MODAL ─────────
class InvitacionModal(discord.ui.Modal, title="Solicitud de Invitación"):

    motivo = discord.ui.TextInput(
        label="Motivo de la invitación",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    usuario = discord.ui.TextInput(
        label="¿Para quién es la invitación?",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):

        staff_channel = interaction.guild.get_channel(STAFF_CHANNEL_ID)

        embed = discord.Embed(
            title="📩 Nueva solicitud de invitación",
            color=discord.Color.purple()
        )

        embed.add_field(name="Solicitante", value=interaction.user.mention, inline=False)
        embed.add_field(name="Motivo", value=self.motivo.value, inline=False)
        embed.add_field(name="Invitación para", value=self.usuario.value, inline=False)

        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        msg = await staff_channel.send(embed=embed)
        await msg.add_reaction(APPROVE_EMOJI)

        await interaction.response.send_message(
            "Tu solicitud fue enviada al staff 💜",
            ephemeral=True
        )

# ───────── BOTÓN ─────────
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Solicitar Invitación",
        emoji=FORM_EMOJI,
        style=discord.ButtonStyle.primary,
        custom_id="solicitar_invitacion_button"
    )
    async def solicitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(InvitacionModal())

# ───────── COMANDO PARA CREAR EMBED ─────────
@bot.tree.command(name="setembed", description="Crea el embed de solicitudes")
async def setembed(interaction: discord.Interaction):

    channel = interaction.guild.get_channel(SOLICITUDES_CHANNEL_ID)

    embed = discord.Embed(
        title=f"# {EMOJI_SEPARATOR} Solicitudes de Invitación",
        description=f"{EMOJI_STAR}Pulsa el botón para completar el formulario y solicitar permiso.",
        color=discord.Color.purple()
    )

    embed.set_footer(text="Irelia Palace • Sistema oficial de invitaciones")

    view = TicketView()
    await channel.send(embed=embed, view=view)

    await interaction.response.send_message("Embed creado correctamente.", ephemeral=True)

# ───────── APROBACIÓN AUTOMÁTICA ─────────
    @bot.event
    async def on_raw_reaction_add(payload):

        # ❌ Ignorar reacciones del propio bot
        if payload.user_id == bot.user.id:
            return

        # ❌ Solo detectar en canal staff
        if payload.channel_id != STAFF_CHANNEL_ID:
            return

        # ❌ Solo detectar emoji correcto
        if str(payload.emoji) != APPROVE_EMOJI:
            return

        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        channel = guild.get_channel(payload.channel_id)
        if channel is None:
            return

        message = await channel.fetch_message(payload.message_id)

        # ❌ Si ya fue aprobado antes, no hacer nada
        if message.content == "APROBADO":
            return

        if not message.embeds:
            return

        embed = message.embeds[0]

        try:
            solicitante_field = embed.fields[0].value
            solicitante_id = int(
                solicitante_field.replace("<@", "")
                .replace(">", "")
                .replace("!", "")
            )
        except:
            return

        miembro = guild.get_member(solicitante_id)
        if miembro is None:
            return

        # 🔥 Crear invitación
        invite_channel = guild.system_channel or guild.text_channels[0]

        invite = await invite_channel.create_invite(
            max_uses=1,
            unique=True,
            reason="Invitación aprobada por el staff"
        )

        # 🔥 Enviar por DM
        try:
            await miembro.send(
                f"✨ Tu solicitud fue aprobada ✨\n\n"
                f"Aquí tienes tu invitación privada:\n{invite.url}"
            )
        except:
            await channel.send(f"No pude enviar DM a {miembro.mention}")
            return

        # 🔥 Eliminar la reacción del staff
        member_who_reacted = guild.get_member(payload.user_id)
        if member_who_reacted:
            await message.remove_reaction(APPROVE_EMOJI, member_who_reacted)

        # 🔥 Marcar como aprobado para que no vuelva a ejecutarse
        await message.edit(content="APROBADO")

        await channel.send(f"✅ Invitación enviada correctamente a {miembro.mention}")

# ───────── REACCIONES EXISTENTES ─────────
@bot.event
async def on_reaction_add(reaction, user):
    await handle_reaction_add(bot, reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):
    await handle_reaction_remove(bot, reaction, user)

@bot.event
async def on_invite_create(invite):
    # invite.inviter -> el usuario que creó la invitación
    # invite.guild -> el servidor donde se creó
    # invite.delete() -> elimina la invitación

    if invite.inviter.id != bot.user.id:
        try:
            await invite.delete()
            print(f"Se eliminó un enlace de invitación creado por {invite.inviter}")
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar invitación: {e}")


# ───────── RUN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN:", TOKEN)
bot.run(TOKEN)
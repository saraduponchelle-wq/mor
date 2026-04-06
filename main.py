import discord
from discord import app_commands
from events.reaction_add import handle_reaction_add
from events.reaction_remove import handle_reaction_remove
from events.detect import handle_invite_detection
from database.db import setup_db
from database.db_servers import setup_servers_db, get_server
import os

EMOJI_ELY = str(os.getenv("ELY", ""))
EMOJI_FLOWER = str(os.getenv("FLOWER", ""))
EMOJI_SEPARATOR = str(os.getenv("SEPARATOR", ""))
EMOJI_CIRCLE = str(os.getenv("CIRCLE", ""))
EMOJI_HEART = str(os.getenv("HEART", ""))
EMOJI_STAR = str(os.getenv("STAR", ""))

USUARIOS_OBJETIVO = [
    698919436354322632,
    947743342249246731
]

OWNER_ID = 903114752060977202

# ───────── INTENTS ─────────

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True
INTENTS.reactions = True

# ───────── BOT ─────────

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=INTENTS)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands sincronizados")

bot = Bot()

# Estado global del juego (por servidor en el futuro si se necesita)
bot.jugadores = []
bot.mensaje_registro = None
bot.NOMBRE_ROL = "Jugador"
bot.silence_mode = False
bot.diversion_activo = False

# ───────── ON READY ─────────

@bot.event
async def on_ready():
    setup_db()
    setup_servers_db()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Feliz San Valentin💘"
        ),
        status=discord.Status.online
    )
    print(f"🤖 Bot conectado como {bot.user}")

# ───────── BOOST ─────────

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.premium_since is None and after.premium_since is not None:
        config = get_server(after.guild.id)
        if not config:
            return
        channel_id = config.get("boost_channel_id")
        if not channel_id:
            return
        channel = after.guild.get_channel(channel_id)
        if channel is None:
            return

        embed = discord.Embed(
            title=f"{EMOJI_FLOWER} Un nuevo impulso para el servidor {EMOJI_FLOWER}",
            description=(
                f"(づ๑•ᴗ•๑)づ {after.mention} ¡Muchas gracias por el boost! {EMOJI_HEART}\n\n"
                f"# {EMOJI_HEART} Tus beneficios:\n"
                f"   {EMOJI_ELY} Un rol totalmente personalizado\n"
                f"   {EMOJI_ELY} Ganar 1000 de dinero diario usando collect income.\n"
                f"   {EMOJI_ELY} Mención de @everyone cuando busques rol."
            ),
            color=discord.Color.from_rgb(186, 85, 211)
        )
        embed.set_thumbnail(url=after.display_avatar.url)
        embed.set_footer(text="Gracias por tu apoyo ✨")
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)

# ───────── DESPEDIDA ─────────

@bot.event
async def on_member_remove(member: discord.Member):
    config = get_server(member.guild.id)
    if not config:
        return
    channel_id = config.get("leave_channel_id")
    if not channel_id:
        return
    channel = member.guild.get_channel(channel_id)
    if channel is None:
        return

    embed = discord.Embed(
        title=f"**{EMOJI_FLOWER} Una despedida {EMOJI_FLOWER}**",
        description=(
            f"{member.mention}\n\n"
            f"{EMOJI_ELY} **Gracias** por haber formado parte de **{member.guild.name}**.\n"
            f"{EMOJI_ELY} Que la diosa **Mor** ilumine tu camino, dondequiera que continúe tu historia. ✨"
        ),
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Que Mor te acompañe")
    await channel.send(embed=embed)

# ───────── BIENVENIDA ─────────

REGLAS_CHANNEL_ID = 1447704211927335016
ROLES_CHANNEL_ID = 1449194573493702726
GENERAL_CHANNEL_ID = 1447695182693798042
SOPORTE_CHANNEL_ID = 1447716741458296962

@bot.event
async def on_member_join(member: discord.Member):
    config = get_server(member.guild.id)
    if not config:
        return
    channel_id = config.get("welcome_channel_id")
    if not channel_id:
        return
    channel = member.guild.get_channel(channel_id)
    if channel is None:
        return

    reglas = f"<#{REGLAS_CHANNEL_ID}>"
    roles = f"<#{ROLES_CHANNEL_ID}>"
    general = f"<#{GENERAL_CHANNEL_ID}>"
    soporte = f"<#{SOPORTE_CHANNEL_ID}>"

    mensaje = (
        f"# {EMOJI_FLOWER} Bienvenido a {member.guild.name} {EMOJI_FLOWER}\n"
        f"{EMOJI_ELY} Estamos **felices** de tenerte entre nosotros, {member.mention}\n\n"
        f"{EMOJI_ELY} **Antes de comenzar, te invitamos a leer nuestras reglas** en {reglas}\n"
        f"{EMOJI_ELY} **¿Tienes alguna duda?** Si no encuentras la respuesta, el equipo estará encantado de asistirte en {soporte}\n"
        f"{EMOJI_ELY} **Pasa a saludarnos en {general},** nos encanta dar la bienvenida a nuestros nuevos miembros.\n"
        f"{EMOJI_ELY} **Si deseas personalizar tu experiencia,** no olvides obtener tus roles en {roles}"
    )

    embed = discord.Embed(
        title=f"**{EMOJI_SEPARATOR} • Una nueva historia comienza!**",
        description=(
            "Que la diosa **Mor** te bendiga y haga de tu viaje dentro de "
            f"**{member.guild.name}** un sueño inolvidable."
        ),
        color=discord.Color.pink()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Bienvenido a {member.guild.name}")
    await channel.send(mensaje, embed=embed)

# ───────── MENSAJES ─────────

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await handle_invite_detection(bot, message)

    if bot.diversion_activo and message.author.id in USUARIOS_OBJETIVO:
        try:
            await message.add_reaction("🫃")
        except Exception:
            pass

# ───────── REACCIONES ─────────

@bot.event
async def on_reaction_add(reaction, user):
    await handle_reaction_add(bot, reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):
    await handle_reaction_remove(bot, reaction, user)

# ───────── CONTROL DE INVITACIONES ─────────

@bot.event
async def on_invite_create(invite):
    if not invite.guild:
        return

    # Si la invitación la creó el propio bot, permitirla
    if invite.inviter and invite.inviter.id == bot.user.id:
        return

    config = get_server(invite.guild.id)
    if not config or not config.get("invitation_control_active"):
        return

    try:
        await invite.delete(reason="Control de invitaciones activo: solo el bot puede crearlas.")
        print(f"[INVITE] Eliminada invitación de {invite.inviter} en {invite.guild.name}")
    except Exception as e:
        print(f"[ERROR] No se pudo eliminar invitación: {e}")

# ───────── SILENCIO ─────────

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if bot.silence_mode and interaction.user.id != OWNER_ID:
        if interaction.type == discord.InteractionType.application_command:
            await interaction.response.send_message(
                "🤫 El silencio reina ahora mismo…",
                ephemeral=True
            )
            return

# ───────── SISTEMA DE SOLICITUDES DE INVITACIÓN ─────────

APPROVE_EMOJI = "✅"
FORM_EMOJI = "📝"

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
        config = get_server(interaction.guild.id)
        if not config:
            await interaction.response.send_message("❌ Este servidor no está configurado.", ephemeral=True)
            return

        staff_channel_id = config.get("review_channel_id")
        if not staff_channel_id:
            await interaction.response.send_message(
                "❌ No hay canal de revisión configurado. Pide a un admin que use `/set_review`.",
                ephemeral=True
            )
            return

        staff_channel = interaction.guild.get_channel(staff_channel_id)
        if not staff_channel:
            await interaction.response.send_message("❌ Canal de revisión no encontrado.", ephemeral=True)
            return

        embed = discord.Embed(title="📩 Nueva solicitud de invitación", color=discord.Color.purple())
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


@bot.tree.command(name="setembed", description="Crea el embed de solicitudes de invitación")
async def setembed(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Solo administradores.", ephemeral=True)
        return

    config = get_server(interaction.guild.id)
    solicitudes_channel_id = config.get("embed_invitation_id") if config else None
    channel = interaction.guild.get_channel(solicitudes_channel_id) if solicitudes_channel_id else interaction.channel

    embed = discord.Embed(
        title=f"# {EMOJI_SEPARATOR} Solicitudes de Invitación",
        description=f"{EMOJI_STAR} Pulsa el botón para completar el formulario y solicitar permiso.",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Sistema oficial de invitaciones")

    await channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("✅ Embed creado correctamente.", ephemeral=True)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if str(payload.emoji) != APPROVE_EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    config = get_server(guild.id)
    if not config:
        return

    if payload.channel_id != config.get("review_channel_id"):
        return

    channel = guild.get_channel(payload.channel_id)
    if not channel:
        return

    message = await channel.fetch_message(payload.message_id)
    if message.content == "APROBADO":
        return
    if not message.embeds:
        return

    embed = message.embeds[0]
    try:
        solicitante_field = embed.fields[0].value
        solicitante_id = int(
            solicitante_field.replace("<@", "").replace(">", "").replace("!", "")
        )
    except Exception:
        return

    miembro = guild.get_member(solicitante_id)
    if miembro is None:
        return

    invite_channel = guild.system_channel or guild.text_channels[0]
    invite = await invite_channel.create_invite(
        max_uses=1,
        unique=True,
        reason="Invitación aprobada por el staff"
    )

    try:
        await miembro.send(
            f"✨ Tu solicitud fue aprobada ✨\n\n"
            f"Aquí tienes tu invitación privada:\n{invite.url}"
        )
    except Exception:
        await channel.send(f"No pude enviar DM a {miembro.mention}")
        return

    member_who_reacted = guild.get_member(payload.user_id)
    if member_who_reacted:
        await message.remove_reaction(APPROVE_EMOJI, member_who_reacted)

    await message.edit(content="APROBADO")
    await channel.send(f"✅ Invitación enviada correctamente a {miembro.mention}")

# ───────── COMANDOS ─────────

from comands.diversion import diversion
from comands.server_config import (
    set_welcome, set_leave, set_spam,
    set_review, set_boost,
    active_defense, active_invitation,
    server_config
)

bot.tree.add_command(diversion)
bot.tree.add_command(set_welcome)
bot.tree.add_command(set_leave)
bot.tree.add_command(set_spam)
bot.tree.add_command(set_review)
bot.tree.add_command(set_boost)
bot.tree.add_command(active_defense)
bot.tree.add_command(active_invitation)
bot.tree.add_command(server_config)

# Descomenta los que quieras activar:
# from comands.start import start
# from comands.end import end
# from comands.girar import girar
# from comands.orden import orden
# from comands.reto import reto
# from comands.silence import silence
# from comands.punition import punition
# from comands.kiss import beso
# from comands.join import join
# from comands.kick import kick
# from comands.salonp import salonp_group
# from comands.embed import evento_amor
# from comands.sanvalentin.confesion import confesion
# from comands.sanvalentin.invitar import sanvalentin
# from comands.adorar import adorar
# from comands.help import help_cmd
# from menus.menu import menu_group
# bot.tree.add_command(start)
# ... etc

# ───────── RUN ─────────

TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN:", TOKEN[:10] + "..." if TOKEN else "NO TOKEN")
bot.run(TOKEN)

import discord
import re
import time
import asyncio

# CONFIGURACIÓN
ROL_PERMITIDO_ID = 1482399459651485737
CANAL_LOG_ID = 1482399939131740353

INVITE_REGEX = r"(discord\.gg\/\S+|discord\.com\/invite\/\S+)"

infracciones = {}


async def silenciar_temporal(canal, miembro, segundos):

    overwrite = canal.overwrites_for(miembro)
    overwrite.send_messages = False
    overwrite.add_reactions = False

    await canal.set_permissions(miembro, overwrite=overwrite)

    await asyncio.sleep(segundos)

    overwrite.send_messages = None
    overwrite.add_reactions = None
    await canal.set_permissions(miembro, overwrite=overwrite)


async def handle_invite_detection(bot, message: discord.Message):

    if message.author.bot:
        return

    # ignorar roles permitidos
    if any(role.id == ROL_PERMITIDO_ID for role in message.author.roles):
        return

    match = re.search(INVITE_REGEX, message.content)

    if not match:
        return

    invite_link = match.group(0)
    usuario = message.author
    canal = message.channel
    guild = message.guild
    log_canal = guild.get_channel(CANAL_LOG_ID)

    ahora = time.time()

    await message.delete()

    # si ya tenía infracción reciente → BAN
    if usuario.id in infracciones and ahora - infracciones[usuario.id] < 600:

        try:
            await guild.ban(usuario, reason="Spam de invitaciones")
        except:
            pass

        if log_canal:
            await log_canal.send(
                f"🚨 **Usuario baneado por spam de invitaciones**\n"
                f"👤 {usuario} ({usuario.id})\n"
                f"🔗 Link enviado: {invite_link}\n\n"
                "@everyone",
                allowed_mentions=discord.AllowedMentions(everyone=True)
            )

        return

    # guardar infracción
    infracciones[usuario.id] = ahora

    # aviso usuario
    try:
        await canal.send(
            f"{usuario.mention} ⚠️ No está permitido enviar links de otros servidores.\n"
            "Has sido silenciado **5 minutos**."
        )
    except:
        pass

    # aviso logs
    if log_canal:
        await log_canal.send(
            f"⚠️ **Intento de invitación detectado**\n"
            f"👤 Usuario: {usuario} ({usuario.id})\n"
            f"🔗 Link enviado: {invite_link}\n\n"
            "@everyone",
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )

    await silenciar_temporal(canal, usuario, 300)
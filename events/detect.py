import discord
import re
import time
import asyncio
from database.db_servers import get_server

INVITE_REGEX = r"(discord\.gg\/\S+|discord\.com\/invite\/\S+)"

# Diccionario de infracciones por servidor: {server_id: {user_id: timestamp}}
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

    guild = message.guild
    if not guild:
        return

    config = get_server(guild.id)
    if not config or not config.get("defense_active"):
        return

    # Verificar si tiene un rol que lo exima (puedes adaptarlo por servidor más adelante)
    ROL_PERMITIDO_ID = getattr(bot, "ROL_PERMITIDO_ID", None)
    if ROL_PERMITIDO_ID and any(role.id == ROL_PERMITIDO_ID for role in message.author.roles):
        return

    match = re.search(INVITE_REGEX, message.content)
    if not match:
        return

    invite_link = match.group(0)
    usuario = message.author
    canal = message.channel
    log_canal_id = config.get("spam_channel_id")
    log_canal = guild.get_channel(log_canal_id) if log_canal_id else None

    ahora = time.time()
    await message.delete()

    servidor_infracciones = infracciones.setdefault(guild.id, {})

    if usuario.id in servidor_infracciones and ahora - servidor_infracciones[usuario.id] < 600:
        try:
            await guild.ban(usuario, reason="Spam de invitaciones")
        except Exception:
            pass

        if log_canal:
            await log_canal.send(
                f"🚨 **Usuario baneado por spam de invitaciones**\n"
                f"👤 {usuario} ({usuario.id})\n"
                f"🔗 Link enviado: `{invite_link}`\n\n"
                "@everyone",
                allowed_mentions=discord.AllowedMentions(everyone=True)
            )
        return

    servidor_infracciones[usuario.id] = ahora

    try:
        await canal.send(
            f"{usuario.mention} ⚠️ No está permitido enviar links de otros servidores.\n"
            "Has sido silenciado **5 minutos**."
        )
    except Exception:
        pass

    if log_canal:
        await log_canal.send(
            f"⚠️ **Intento de invitación detectado**\n"
            f"👤 Usuario: {usuario} ({usuario.id})\n"
            f"🔗 Link enviado: `{invite_link}`\n\n"
            "@everyone",
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )

    await silenciar_temporal(canal, usuario, 300)

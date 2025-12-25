import discord

NOMBRE_ROL = "Ruleta"
CANAL_RULETA_ID = 1447699143417135145
OWNER_ID = 903114752060977202

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

async def handle_reaction_add(bot, reaction, user):
    if user.bot or not bot.mensaje_registro:
        return

    if reaction.message.id != bot.mensaje_registro.id:
        return

    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if not rol or member in bot.jugadores:
        return

    bot.jugadores.append(member)
    await member.add_roles(rol)

    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(f"👑✨ {EMOJI_JIJI} **Mi creadora ha entrado a la ruleta.**")
        else:
            await canal.send(f"{EMOJI_RANDOM} {member.mention} se unió a la ruleta.")

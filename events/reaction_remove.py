import discord

NOMBRE_ROL = "Ruleta"
CANAL_RULETA_ID = 1447699143417135145
OWNER_ID = 903114752060977202

EMOJI_ENOJO = "<:enojo:1451014466547220561>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

async def on_reaction_remove(reaction, user):
    bot = reaction.message._state._get_client()

    if user.bot or not bot.mensaje_registro:
        return
    if reaction.message.id != bot.mensaje_registro.id:
        return
    if str(reaction.emoji) != "🎉":
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    if member not in bot.jugadores:
        return

    bot.jugadores.remove(member)
    await member.remove_roles(rol)

    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(
                f"🕯️👑 {EMOJI_JIJI} **Mi creadora ha salido de la ruleta.**"
            )
        else:
            await canal.send(
                f"{EMOJI_ENOJO} {member.mention} salió de la ruleta."
            )

import discord
from discord import app_commands

NOMBRE_ROL = "Ruleta"
CANAL_RULETA_ID = 1447699143417135145
OWNER_ID = 903114752060977202

EMOJI_RANDOM = "<a:random:1451014515473911828>"
EMOJI_JIJI = "<:jiji:1451013733513035920>"

@app_commands.command(name="join", description="unete a la ruleta")
async def join(interaction: discord.Interaction):
    bot = interaction.client
    guild = interaction.guild

    # ❌ No hay ruleta activa
    if not bot.mensaje_registro:
        await interaction.response.send_message(
            "❌ No hay ruletas activas, VETE!",
            ephemeral=True
        )
        return

    member = interaction.user
    rol = discord.utils.get(guild.roles, name=NOMBRE_ROL)

    # Ya está dentro
    if member in bot.jugadores:
        await interaction.response.send_message(
            "🎲 Ya estas dentro...",
            ephemeral=True
        )
        return

    # Añadir jugador
    bot.jugadores.append(member)
    if rol:
        await member.add_roles(rol)

    await interaction.response.send_message(
        "🎉 Te haz unido a la ruleta!"
    )

    canal = guild.get_channel(CANAL_RULETA_ID)
    if canal:
        if member.id == OWNER_ID:
            await canal.send(f"👑✨ {EMOJI_JIJI} **Nuestra diosa se a unido.**")
        else:
            await canal.send(f"{EMOJI_RANDOM} {member.mention} se a unido a la ruleta.")

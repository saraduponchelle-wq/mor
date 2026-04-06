import discord
from discord import app_commands
from database.db_servers import set_server_field, get_server, ensure_server

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Solo los administradores pueden usar este comando.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)


@app_commands.command(name="set_welcome", description="Establece el canal de bienvenida")
@app_commands.describe(canal="Canal donde se enviarán los mensajes de bienvenida")
@is_admin()
async def set_welcome(interaction: discord.Interaction, canal: discord.TextChannel):
    set_server_field(interaction.guild.id, "welcome_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de bienvenida establecido en {canal.mention}",
        ephemeral=True
    )


@app_commands.command(name="set_leave", description="Establece el canal de despedidas")
@app_commands.describe(canal="Canal donde se enviarán los mensajes de despedida")
@is_admin()
async def set_leave(interaction: discord.Interaction, canal: discord.TextChannel):
    set_server_field(interaction.guild.id, "leave_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de despedidas establecido en {canal.mention}",
        ephemeral=True
    )


@app_commands.command(name="set_spam", description="Establece el canal de logs de spam/invitaciones detectadas")
@app_commands.describe(canal="Canal donde se registrarán los intentos de spam")
@is_admin()
async def set_spam(interaction: discord.Interaction, canal: discord.TextChannel):
    set_server_field(interaction.guild.id, "spam_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de logs de spam establecido en {canal.mention}",
        ephemeral=True
    )


@app_commands.command(name="set_review", description="Establece el canal donde llegan las solicitudes de invitación")
@app_commands.describe(canal="Canal donde el staff revisará las solicitudes")
@is_admin()
async def set_review(interaction: discord.Interaction, canal: discord.TextChannel):
    set_server_field(interaction.guild.id, "review_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de revisión de solicitudes establecido en {canal.mention}",
        ephemeral=True
    )


@app_commands.command(name="set_boost", description="Establece el canal de notificaciones de boost")
@app_commands.describe(canal="Canal donde se anunciarán los boosts")
@is_admin()
async def set_boost(interaction: discord.Interaction, canal: discord.TextChannel):
    set_server_field(interaction.guild.id, "boost_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de boosts establecido en {canal.mention}",
        ephemeral=True
    )


@app_commands.command(name="active_defense", description="Activa o desactiva la defensa anti-invitaciones externas")
@app_commands.describe(modo="on para activar, off para desactivar")
@is_admin()
async def active_defense(interaction: discord.Interaction, modo: str):
    modo = modo.lower()
    if modo not in ("on", "off"):
        await interaction.response.send_message("⚠️ Usa `on` o `off`.", ephemeral=True)
        return

    activo = modo == "on"
    set_server_field(interaction.guild.id, "defense_active", activo)

    estado = "✅ activada" if activo else "❌ desactivada"
    await interaction.response.send_message(
        f"🛡️ Defensa anti-spam **{estado}**.\n"
        f"{'Los links de invitación externos serán eliminados automáticamente.' if activo else 'Ya no se bloquearán links externos.'}",
        ephemeral=True
    )


@app_commands.command(name="active_invitation", description="Activa o desactiva el control de invitaciones del servidor")
@app_commands.describe(modo="on para activar, off para desactivar")
@is_admin()
async def active_invitation(interaction: discord.Interaction, modo: str):
    modo = modo.lower()
    if modo not in ("on", "off"):
        await interaction.response.send_message("⚠️ Usa `on` o `off`.", ephemeral=True)
        return

    activo = modo == "on"
    set_server_field(interaction.guild.id, "invitation_control_active", activo)

    estado = "✅ activado" if activo else "❌ desactivado"
    await interaction.response.send_message(
        f"🔒 Control de invitaciones **{estado}**.\n"
        f"{'Solo el bot podrá crear invitaciones. Las demás serán eliminadas automáticamente.' if activo else 'Los miembros pueden crear invitaciones libremente.'}",
        ephemeral=True
    )


@app_commands.command(name="server_config", description="Muestra la configuración actual del servidor")
@is_admin()
async def server_config(interaction: discord.Interaction):
    ensure_server(interaction.guild.id)
    config = get_server(interaction.guild.id)

    def fmt_channel(cid):
        if cid:
            ch = interaction.guild.get_channel(cid)
            return ch.mention if ch else f"ID: {cid} (no encontrado)"
        return "No configurado"

    embed = discord.Embed(
        title="⚙️ Configuración del servidor",
        color=discord.Color.blurple()
    )
    embed.add_field(name="👋 Bienvenida", value=fmt_channel(config["welcome_channel_id"]), inline=False)
    embed.add_field(name="🚪 Despedidas", value=fmt_channel(config["leave_channel_id"]), inline=False)
    embed.add_field(name="🚨 Logs de spam", value=fmt_channel(config["spam_channel_id"]), inline=False)
    embed.add_field(name="📋 Revisión de solicitudes", value=fmt_channel(config["review_channel_id"]), inline=False)
    embed.add_field(name="💜 Boosts", value=fmt_channel(config["boost_channel_id"]), inline=False)
    embed.add_field(name="🛡️ Defensa anti-spam", value="✅ Activa" if config["defense_active"] else "❌ Inactiva", inline=True)
    embed.add_field(name="🔒 Control de invitaciones", value="✅ Activo" if config["invitation_control_active"] else "❌ Inactivo", inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=True)

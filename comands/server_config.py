import discord
from discord import app_commands
from database.db_servers import set_server_field, get_server, ensure_server


# ── Helper: verificar admin ──────────────────────────────────────────────────

async def check_admin(interaction: discord.Interaction) -> bool:
    """Devuelve True si el usuario es admin, responde con error si no lo es."""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Solo los administradores pueden usar este comando.",
            ephemeral=True
        )
        return False
    return True


# ── /set_welcome ─────────────────────────────────────────────────────────────

@app_commands.command(name="set_welcome", description="Establece el canal de bienvenida")
@app_commands.describe(canal="Canal donde se enviarán los mensajes de bienvenida")
async def set_welcome(interaction: discord.Interaction, canal: discord.TextChannel):
    if not await check_admin(interaction):
        return
    set_server_field(interaction.guild.id, "welcome_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de bienvenida establecido en {canal.mention}", ephemeral=True
    )


# ── /set_leave ───────────────────────────────────────────────────────────────

@app_commands.command(name="set_leave", description="Establece el canal de despedidas")
@app_commands.describe(canal="Canal donde se enviarán los mensajes de despedida")
async def set_leave(interaction: discord.Interaction, canal: discord.TextChannel):
    if not await check_admin(interaction):
        return
    set_server_field(interaction.guild.id, "leave_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de despedidas establecido en {canal.mention}", ephemeral=True
    )


# ── /set_spam ────────────────────────────────────────────────────────────────

@app_commands.command(name="set_spam", description="Establece el canal de logs de spam")
@app_commands.describe(canal="Canal donde se registrarán los intentos de spam")
async def set_spam(interaction: discord.Interaction, canal: discord.TextChannel):
    if not await check_admin(interaction):
        return
    set_server_field(interaction.guild.id, "spam_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de logs de spam establecido en {canal.mention}", ephemeral=True
    )


# ── /set_review ──────────────────────────────────────────────────────────────

@app_commands.command(name="set_review", description="Establece el canal de revisión de solicitudes de invitación")
@app_commands.describe(canal="Canal donde el staff revisará las solicitudes")
async def set_review(interaction: discord.Interaction, canal: discord.TextChannel):
    if not await check_admin(interaction):
        return
    set_server_field(interaction.guild.id, "review_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de revisión establecido en {canal.mention}", ephemeral=True
    )


# ── /set_boost ───────────────────────────────────────────────────────────────

@app_commands.command(name="set_boost", description="Establece el canal de notificaciones de boost")
@app_commands.describe(canal="Canal donde se anunciarán los boosts")
async def set_boost(interaction: discord.Interaction, canal: discord.TextChannel):
    if not await check_admin(interaction):
        return
    set_server_field(interaction.guild.id, "boost_channel_id", canal.id)
    await interaction.response.send_message(
        f"✅ Canal de boosts establecido en {canal.mention}", ephemeral=True
    )


# ── /active_defense ──────────────────────────────────────────────────────────

@app_commands.command(name="active_defense", description="Activa o desactiva el bloqueo de links de invitación externos")
@app_commands.describe(modo="on para activar, off para desactivar")
async def active_defense(interaction: discord.Interaction, modo: str):
    if not await check_admin(interaction):
        return

    modo = modo.lower().strip()
    if modo not in ("on", "off"):
        await interaction.response.send_message("⚠️ Usa `on` o `off`.", ephemeral=True)
        return

    activo = (modo == "on")
    set_server_field(interaction.guild.id, "defense_active", activo)

    if activo:
        msg = (
            "🛡️ **Defensa anti-spam activada.**\n"
            "Los links de invitación externos serán eliminados automáticamente.\n"
            "Los usuarios reincidentes serán baneados."
        )
    else:
        msg = (
            "🛡️ **Defensa anti-spam desactivada.**\n"
            "Ya no se bloquearán links de servidores externos."
        )

    await interaction.response.send_message(msg, ephemeral=True)


# ── /active_invitation ───────────────────────────────────────────────────────

@app_commands.command(name="active_invitation", description="Activa o desactiva el control de invitaciones (solo el bot puede crearlas)")
@app_commands.describe(modo="on para activar, off para desactivar")
async def active_invitation(interaction: discord.Interaction, modo: str):
    if not await check_admin(interaction):
        return

    modo = modo.lower().strip()
    if modo not in ("on", "off"):
        await interaction.response.send_message("⚠️ Usa `on` o `off`.", ephemeral=True)
        return

    activo = (modo == "on")
    set_server_field(interaction.guild.id, "invitation_control_active", activo)

    if activo:
        msg = (
            "🔒 **Control de invitaciones activado.**\n"
            "Solo el bot podrá crear invitaciones.\n"
            "Cualquier otra invitación creada será eliminada automáticamente."
        )
    else:
        msg = (
            "🔓 **Control de invitaciones desactivado.**\n"
            "Los miembros pueden volver a crear invitaciones libremente."
        )

    await interaction.response.send_message(msg, ephemeral=True)


# ── /server_config ───────────────────────────────────────────────────────────

@app_commands.command(name="server_config", description="Muestra la configuración actual del servidor")
async def server_config(interaction: discord.Interaction):
    if not await check_admin(interaction):
        return

    ensure_server(interaction.guild.id)
    config = get_server(interaction.guild.id)

    def fmt_channel(cid):
        if cid:
            ch = interaction.guild.get_channel(int(cid))
            return ch.mention if ch else f"⚠️ Canal no encontrado (ID: {cid})"
        return "❌ No configurado"

    def fmt_bool(val):
        return "✅ Activo" if val else "❌ Inactivo"

    embed = discord.Embed(
        title="⚙️ Configuración del servidor",
        color=discord.Color.blurple()
    )
    embed.add_field(name="👋 Bienvenida",              value=fmt_channel(config.get("welcome_channel_id")),    inline=False)
    embed.add_field(name="🚪 Despedidas",              value=fmt_channel(config.get("leave_channel_id")),      inline=False)
    embed.add_field(name="🚨 Logs de spam",            value=fmt_channel(config.get("spam_channel_id")),       inline=False)
    embed.add_field(name="📋 Revisión de solicitudes", value=fmt_channel(config.get("review_channel_id")),     inline=False)
    embed.add_field(name="💜 Boosts",                  value=fmt_channel(config.get("boost_channel_id")),      inline=False)
    embed.add_field(name="🛡️ Defensa anti-spam",      value=fmt_bool(config.get("defense_active")),           inline=True)
    embed.add_field(name="🔒 Control invitaciones",    value=fmt_bool(config.get("invitation_control_active")), inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=True)

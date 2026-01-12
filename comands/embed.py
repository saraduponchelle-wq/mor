import discord
from discord import app_commands

@app_commands.command(
    name="embed",
    description="Muestra el anuncio de novedades del bot"
)
@app_commands.checks.has_permissions(administrator=True)
async def embed_anuncio(interaction: discord.Interaction):

    # ==========================
    # EMBED 1 — RULETA
    # ==========================

    embed_ruleta = discord.Embed(
        title="🎰 Nuevos comandos de la ruleta",
        description=(
            "¡Hoy se integraron **nuevas funciones** para la ruleta!\n\n"
            "Ahora puedes **unirte o salir fácilmente** usando los nuevos comandos:"
        ),
        color=discord.Color.red()
    )

    embed_ruleta.add_field(
        name="🆕 Comandos añadidos",
        value=(
            "• `/ruleta join`\n"
            "• `/ruleta kick`"
        ),
        inline=False
    )

    await interaction.response.send_message(embed=embed_ruleta)

    # ==========================
    # EMBED 2 — SALONES PRIVADOS
    # ==========================

    embed_salonp = discord.Embed(
        title="🏠 Nueva modalidad: Salones Privados",
        description=(
            "Ahora puedes **crear grupos privados fácilmente** para rol.\n\n"
            "Son ideales para usar **Tupperbox**, cambiar de perfil "
            "y tener una experiencia de rol más inmersiva.\n\n"
            "Los salones son **privados**: solo los miembros pueden verlos.\n"
            "Los **admins** pueden supervisar lo que ocurre."
        ),
        color=discord.Color.blurple()
    )

    embed_salonp.add_field(
        name="📜 Comandos disponibles",
        value=(
            "• `/salonp create`\n"
            "• `/salonp invite`\n"
            "• `/salonp eliminate`"
        ),
        inline=False
    )

    await interaction.followup.send(embed=embed_salonp)
    await interaction.followup.send("@everyone")

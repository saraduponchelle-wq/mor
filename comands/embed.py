import discord
from discord.ext import commands

@commands.has_permissions(administrator=True)
@commands.command(name="embed")
async def embed_anuncio(ctx: commands.Context):

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
            "• `/ruleta join` → Unirte a la ruleta\n"
            "• `/ruleta kick` → Salir de la ruleta"
        ),
        inline=False
    )

    await ctx.send(embed=embed_ruleta)

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
            "• `/salonp invite @usuario`\n"
            "• `/salonp eliminate @usuario`"
        ),
        inline=False
    )

    await ctx.send(embed=embed_salonp)

    # ==========================
    # MENCIÓN FINAL
    # ==========================

    await ctx.send("@everyone")

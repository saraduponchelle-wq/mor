import discord
from discord import app_commands
import os

@app_commands.command(
    name="embed",
    description="Publica el anuncio del evento de Minecraft"
)
@app_commands.checks.has_permissions(administrator=True)
async def embed_anuncio(interaction: discord.Interaction):

    # ⏳ Evita el error 10062
    await interaction.response.defer()

    embed = discord.Embed(
        title="⛏️🏰 EVENTO DE MINECRAFT – CONSTRUCCIÓN EN EQUIPO 🏰⛏️",
        description=(
            "**¡Tenemos grandes noticias! 🎉**\n"
            "Recientemente hemos abierto el servidor de Minecraft, y para celebrarlo "
            "traemos un evento especial donde la creatividad y el trabajo en equipo serán la clave."
        ),
        color=discord.Color.dark_green()
    )

    embed.add_field(
        name="🧱 OBJETIVO DEL EVENTO",
        value=(
            "El objetivo es **crear la mejor base de Minecraft** antes del **próximo domingo**.\n"
            "Pueden participar **solos o en grupo**, planear juntos y construir la base que más impresione."
        ),
        inline=False
    )

    embed.add_field(
        name="👨‍⚖️ EVALUACIÓN",
        value=(
            "El **domingo**, un **jurado** evaluará cada base teniendo en cuenta:\n"
            "• Creatividad\n"
            "• Diseño\n"
            "• Detalles\n"
            "• Trabajo en equipo\n\n"
            "De ahí saldrán los ganadores 🏆"
        ),
        inline=False
    )

    embed.add_field(
        name="🎁 PREMIOS",
        value=(
            "🥇 **Primer lugar**\n"
            "• 1 mes de **Discord Nitro** *(solo 1 persona del equipo)*\n"
            "• Rol de **Primer Lugar**\n\n"
            "🥈 **Segundo lugar**\n"
            "• **Marco de la tienda** *(solo 1 persona del equipo)*\n"
            "• Rol de **Segundo Lugar**\n\n"
            "🥉 **Tercer lugar**\n"
            "• Rol de **Tercer Lugar**"
        ),
        inline=False
    )

    embed.add_field(
        name="⚠️ IMPORTANTE",
        value=(
            "Si el equipo ganador tiene varios integrantes, "
            "**solo una persona podrá recibir el Nitro o el marco**.\n"
            "Los **roles** se otorgarán según el puesto obtenido."
        ),
        inline=False
    )

    embed.add_field(
        name="📅 FECHA LÍMITE",
        value=(
            "Tienen hasta el **domingo** para terminar su base.\n"
            "Ese mismo día se realizará la evaluación y se anunciarán los ganadores."
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 ACCESO AL SERVIDOR DE MINECRAFT",
        value=(
            "Pueden conseguir el **rol de Minecraft** para tener acceso al canal correspondiente "
            "**yendo al chat de roles**."
        ),
        inline=False
    )

    embed.set_footer(text="✨ Patrocinado por Mor ✨")

    gif_path = "data/embed.gif"

    # 📌 ORDEN FINAL: EMBED → GIF → @everyone
    await interaction.followup.send(
        content="@everyone",
        embed=embed,
        file=discord.File(gif_path) if os.path.exists(gif_path) else None
    )

import discord

MENU_COMIDA = {
    "Hamburguesa": 500,
    "Pizza": 700,
    "Hot Dog": 300
}

MESEROS_ROLE_ID = 123456789012345678  # pon el ID real


async def enviar_menu_comida(ctx):
    embed = discord.Embed(
        title="🍔 Menú de Comida",
        description="Selecciona lo que deseas pedir",
        color=discord.Color.orange()
    )

    for nombre, precio in MENU_COMIDA.items():
        embed.add_field(
            name=nombre,
            value=f"💰 {precio} monedas\n🛒 `/item buy {nombre}`",
            inline=False
        )

    await ctx.send(embed=embed)

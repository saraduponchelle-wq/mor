import discord

MENU_BAR = {
    "Cerveza": 250,
    "Vino": 600,
    "Whisky": 1200
}

MESEROS_ROLE_ID = 123456789012345678


async def enviar_menu_bar(ctx):
    embed = discord.Embed(
        title="🍸 Carta del Bar",
        description="Bebidas disponibles",
        color=discord.Color.purple()
    )

    for nombre, precio in MENU_BAR.items():
        embed.add_field(
            name=nombre,
            value=f"💰 {precio} monedas\n🛒 `/item buy {nombre}`",
            inline=False
        )

    await ctx.send(embed=embed)

import discord
from discord.ext import commands
import json

MENU_FILE = "data/menu_comida.json"
MESERO_ROLE_NAME = "Meser@"


# ---------- VIEW ----------
class MenuComidaView(discord.ui.View):
    def __init__(self, author_id: int, monedas: int | None, menu: dict):
        super().__init__(timeout=180)
        self.author_id = author_id

        for p in menu.values():
            puede_comprar = True
            if monedas is not None and p["precio"] > monedas:
                puede_comprar = False

            self.add_item(ComprarButton(author_id, p, puede_comprar))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return False
        return True


# ---------- BOTÓN ----------
class ComprarButton(discord.ui.Button):
    def __init__(self, author_id: int, producto: dict, puede_comprar: bool):
        super().__init__(
            label=f"{producto['nombre']} — {producto['precio']}",
            emoji=producto.get("emoji", "🛒"),
            style=discord.ButtonStyle.success if puede_comprar else discord.ButtonStyle.secondary,
            disabled=not puede_comprar
        )
        self.producto = producto

    async def callback(self, interaction: discord.Interaction):
        p = self.producto

        rol = discord.utils.get(interaction.guild.roles, name=MESERO_ROLE_NAME)

        mensaje = (
            f"🍔 **Nuevo pedido**\n"
            f"👤 Usuario: {interaction.user.mention}\n"
            f"📦 Producto: {p['emoji']} {p['nombre']}\n"
            f"💰 Precio: {p['precio']} monedas\n\n"
            f"👉 **Cobrar con:**\n"
            f"`/item buy {p['nombre']}`"
        )

        if rol:
            mensaje += f"\n{rol.mention}"

        await interaction.channel.send(mensaje)
        await interaction.response.send_message(
            "✅ Pedido enviado a los meseros.",
            ephemeral=True
        )


# ---------- FUNCIÓN PÚBLICA ----------
async def enviar_menu_comida(ctx: commands.Context, monedas: int | None = None):
    try:
        with open(MENU_FILE, encoding="utf-8") as f:
            menu = json.load(f)

        descripcion = (
            "Haz click en un producto para pedirlo.\n"
            "El pago se realiza con `/item buy`."
        )

        if monedas is not None:
            descripcion += f"\n\n💰 **Tus monedas:** {monedas}"

        embed = discord.Embed(
            title="🍔 Menú de Comida",
            description=descripcion,
            color=discord.Color.orange()
        )

        for p in menu.values():
            embed.add_field(
                name=f"{p['emoji']} {p['nombre']}",
                value=f"{p['descripcion']}\n💰 **{p['precio']} monedas**",
                inline=False
            )

        view = MenuComidaView(ctx.author.id, monedas, menu)
        await ctx.send(embed=embed, view=view)

    except Exception as e:
        await ctx.send(f"❌ Error al abrir el menú:\n```{e}```")

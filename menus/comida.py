import discord
from discord import ui
import json

# ───────── CONFIG ─────────

MESEROS_ROLE_ID = 1452528262608850964
COLOR_STORE = 0x2b2d31
DATA_PATH = "data/comida.json"

# ───────── CARGAR JSON ─────────

def cargar_menu():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

MENU_COMIDA = cargar_menu()

# ───────── MODAL NOTA ─────────

class NotaPedidoModal(ui.Modal, title="📝 Nota para el pedido"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        placeholder="Ej: sin cebolla, bien cocido, etc.",
        required=False,
        max_length=200
    )

    def __init__(self, producto):
        super().__init__()
        self.producto = producto

    async def on_submit(self, interaction: discord.Interaction):
        rol = interaction.guild.get_role(MESEROS_ROLE_ID)

        mensaje = (
            f"📢 **Nuevo pedido**\n\n"
            f"{self.producto['emoji']} **Producto:** {self.producto['nombre']}\n"
            f"💰 **Precio:** {self.producto['precio']} monedas\n"
            f"📝 **Nota:** {self.nota.value or 'Sin nota'}\n\n"
            f"{rol.mention if rol else ''}\n"
            f"➡️ Comprar con: `/item buy {self.producto['nombre']}`"
        )

        await interaction.response.send_message(
            mensaje,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

# ───────── SELECT MENU ─────────

class SelectorComida(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=item["nombre"],
                description=f"{item['precio']} monedas",
                emoji=item["emoji"]
            )
            for item in MENU_COMIDA
        ]

        super().__init__(
            placeholder="🍽️ Selecciona tu comida",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        producto = next(
            item for item in MENU_COMIDA
            if item["nombre"] == self.values[0]
        )

        await interaction.response.send_modal(
            NotaPedidoModal(producto)
        )

# ───────── VIEW ─────────

class MenuComidaView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectorComida())

# ───────── FUNCIÓN PARA SLASH ─────────

async def mostrar_menu_comida(
    interaction: discord.Interaction,
    balance: int | None = None
):
    descripcion = (
        "Haz clic en un producto para pedirlo.\n"
        "El pago se realiza con `/item buy`.\n\n"
    )

    if balance is not None:
        descripcion += f"💰 **Tu balance:** {balance} monedas\n\n"

    embed = discord.Embed(
        title="🍔 Menú de Comida",
        description=descripcion,
        color=COLOR_STORE
    )

    for item in MENU_COMIDA:
        embed.add_field(
            name=f"{item['emoji']} **{item['nombre']}**",
            value=(
                f"{item['descripcion']}\n\n"
                f"💰 **{item['precio']} monedas**\n\n"
                "━━━━━━━━━━━━━━"
            ),
            inline=False
        )

    await interaction.response.send_message(
        embed=embed,
        view=MenuComidaView()
    )

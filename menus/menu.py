import discord
from discord import ui, app_commands
import json

# ───────── CONFIG ─────────

MESEROS_ROLE_ID = 1452528262608850964
COLOR_STORE = 0x2b2d31

DATA_COMIDA = "data/comida.json"
DATA_BAR = "data/bar.json"

# ───────── CARGA JSON ─────────

def cargar_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

MENU_COMIDA = cargar_json(DATA_COMIDA)
MENU_BAR = cargar_json(DATA_BAR)

# ───────── MODAL NOTA ─────────

class NotaPedidoModal(ui.Modal, title="📝 Nota para el pedido"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        placeholder="Ej: sin azúcar, extra hielo, etc.",
        required=False,
        max_length=200
    )

    def __init__(self, producto):
        super().__init__()
        self.producto = producto

    async def on_submit(self, interaction: discord.Interaction):
        rol = interaction.guild.get_role(MESEROS_ROLE_ID)

        await interaction.response.send_message(
            (
                f"📢 **Nuevo pedido**\n\n"
                f"{self.producto['emoji']} **Producto:** {self.producto['nombre']}\n"
                f"💰 **Precio:** {self.producto['precio']} monedas\n"
                f"📝 **Nota:** {self.nota.value or 'Sin nota'}\n\n"
                f"{rol.mention if rol else ''}\n"
                f"➡️ Comprar con: `/item buy {self.producto['nombre']}`"
            ),
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

# ───────── SELECT PRODUCTOS ─────────

class SelectorProducto(ui.Select):
    def __init__(self, productos, placeholder):
        options = [
            discord.SelectOption(
                label=p["nombre"],
                description=f"{p['precio']} monedas",
                emoji=p["emoji"]
            )
            for p in productos
        ]

        super().__init__(
            placeholder=placeholder,
            options=options
        )

        self.productos = productos

    async def callback(self, interaction: discord.Interaction):
        producto = next(p for p in self.productos if p["nombre"] == self.values[0])
        await interaction.response.send_modal(NotaPedidoModal(producto))

# ───────── VIEW PRODUCTOS ─────────

class MenuProductosView(ui.View):
    def __init__(self, productos, placeholder):
        super().__init__(timeout=None)
        self.add_item(SelectorProducto(productos, placeholder))

# ───────── SELECT BAR / CAFÉ ─────────

class SelectorTipoMenu(ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="🍽️ ¿Qué deseas ver?",
            options=[
                discord.SelectOption(
                    label="Bar",
                    description="Cócteles y bebidas",
                    emoji="🍸"
                ),
                discord.SelectOption(
                    label="Café",
                    description="Comidas y bebidas calientes",
                    emoji="☕"
                )
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Bar":
            productos = MENU_BAR
            titulo = "🍸 Menú del Bar"
            placeholder = "Selecciona una bebida"
        else:
            productos = MENU_COMIDA
            titulo = "☕ Menú del Café"
            placeholder = "Selecciona un producto"

        embed = discord.Embed(
            title=titulo,
            description="Haz clic para ordenar.\nPago con `/item buy`.",
            color=COLOR_STORE
        )

        for p in productos:
            embed.add_field(
                name=f"{p['emoji']} **{p['nombre']}**",
                value=f"{p['descripcion']}\n💰 **{p['precio']} monedas**",
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            view=MenuProductosView(productos, placeholder)
        )

# ───────── VIEW PRINCIPAL ─────────

class MenuPrincipalView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectorTipoMenu())

# ───────── SLASH COMMAND ─────────

@app_commands.command(
    name="menu",
    description="Muestra el menú del bar o café"
)
async def menu(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Menú",
        description="Selecciona qué menú deseas ver",
        color=COLOR_STORE
    )

    await interaction.response.send_message(
        embed=embed,
        view=MenuPrincipalView()
    )

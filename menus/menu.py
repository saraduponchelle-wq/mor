import discord
from discord import ui, app_commands

# ───────── CONFIG ─────────

MESEROS_ROLE_ID = 1452528262608850964      # ☕ Meseros
BARTENDERS_ROLE_ID = 1453930787928805386   # 🍷 Bartenders (CAMBIA)

COLOR_BAR = 0x6f1d1b
COLOR_CAFE = 0x5a3e2b

# ───────── DATOS ─────────

MENU_BAR = [
    {"id": "vino", "nombre": "Vino Tinto", "precio": 18, "emoji": "🍷"},
    {"id": "mojito", "nombre": "Mojito", "precio": 15, "emoji": "🍹"},
    {"id": "whisky", "nombre": "Whisky", "precio": 22, "emoji": "🥃"},
    {"id": "cerveza", "nombre": "Cerveza Artesanal", "precio": 12, "emoji": "🍺"},
    {"id": "ron", "nombre": "Ron Añejo", "precio": 20, "emoji": "🥃"},
    {"id": "gin", "nombre": "Gin Tonic", "precio": 17, "emoji": "🍸"},
    {"id": "tequila", "nombre": "Tequila", "precio": 19, "emoji": "🥂"},
    {"id": "vodka", "nombre": "Vodka", "precio": 16, "emoji": "🍾"},
]

MENU_CAFE = [
    {"id": "espresso", "nombre": "Espresso", "precio": 7, "emoji": "☕"},
    {"id": "capuccino", "nombre": "Capuccino", "precio": 10, "emoji": "☕"},
    {"id": "americano", "nombre": "Americano", "precio": 8, "emoji": "☕"},
    {"id": "chocolate", "nombre": "Chocolate Caliente", "precio": 9, "emoji": "🍫"},
    {"id": "te", "nombre": "Té Aromático", "precio": 6, "emoji": "🍵"},
    {"id": "frappe", "nombre": "Frappé", "precio": 11, "emoji": "🧋"},
    {"id": "sandwich", "nombre": "Sandwich Mixto", "precio": 14, "emoji": "🥪"},
    {"id": "croissant", "nombre": "Croissant", "precio": 9, "emoji": "🥐"},
]

# ───────── MODAL ─────────

class NotaPedidoModal(ui.Modal, title="📝 Nota para el pedido"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        required=False,
        max_length=200
    )

    def __init__(self, producto, origen):
        super().__init__()
        self.producto = producto
        self.origen = origen

    async def on_submit(self, interaction: discord.Interaction):
        if self.origen == "Bar":
            rol = interaction.guild.get_role(BARTENDERS_ROLE_ID)
            titulo = "🍷 Nuevo pedido del BAR"
        else:
            rol = interaction.guild.get_role(MESEROS_ROLE_ID)
            titulo = "☕ Nuevo pedido del CAFÉ"

        mensaje = (
            f"📢 **{titulo}**\n\n"
            f"{self.producto['emoji']} **Producto:** {self.producto['nombre']}\n"
            f"💰 **Precio:** S/ {self.producto['precio']}\n"
            f"📝 **Nota:** {self.nota.value or 'Sin nota'}\n\n"
            f"{rol.mention if rol else ''}\n"
            f"➡️ Comprar con: `/item buy {self.producto['nombre']}`"
        )

        await interaction.response.send_message(
            mensaje,
            allowed_mentions=discord.AllowedMentions(roles=True),
            delete_after=60
        )

# ───────── SELECT PRODUCTOS ─────────

class SelectorProducto(ui.Select):
    def __init__(self, productos, origen):
        self.productos = productos
        self.origen = origen

        options = [
            discord.SelectOption(
                label=p["nombre"],
                description=f"S/ {p['precio']}",
                emoji=p["emoji"],
                value=p["id"]
            )
            for p in productos
        ]

        super().__init__(
            placeholder="🧾 Selecciona un producto",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        producto = next(p for p in self.productos if p["id"] == self.values[0])

        await interaction.message.delete()
        await interaction.response.send_modal(
            NotaPedidoModal(producto, self.origen)
        )

# ───────── VIEW PRODUCTOS ─────────

class MenuProductosView(ui.View):
    def __init__(self, productos, origen):
        super().__init__(timeout=120)
        self.add_item(SelectorProducto(productos, origen))

# ───────── SELECT PRINCIPAL ─────────

class SelectorMenu(ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="📜 ¿Qué menú deseas ver?",
            options=[
                discord.SelectOption(label="Bar", emoji="🍷"),
                discord.SelectOption(label="Café", emoji="☕"),
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()

        if self.values[0] == "Bar":
            await mostrar_menu(interaction, MENU_BAR, "🍷 Menú del Bar", COLOR_BAR, "Bar")
        else:
            await mostrar_menu(interaction, MENU_CAFE, "☕ Menú del Café", COLOR_CAFE, "Café")

# ───────── VIEW PRINCIPAL ─────────

class MenuPrincipalView(ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(SelectorMenu())

# ───────── FUNCIÓN MOSTRAR MENÚ ─────────

async def mostrar_menu(interaction, productos, titulo, color, origen):
    descripcion = ""

    for p in productos:
        descripcion += (
            f"**{p['emoji']} {p['nombre']}**\n"
            f"S/ {p['precio']}\n"
            "──────────────\n"
        )

    embed = discord.Embed(
        title=titulo,
        description=descripcion,
        color=color
    )

    await interaction.response.send_message(
        embed=embed,
        view=MenuProductosView(productos, origen)
    )

# ───────── SLASH COMMAND ─────────

menu_group = app_commands.Group(
    name="menu",
    description="Menús del local"
)

@menu_group.command(
    name="ver",
    description="Ver el menú del bar o café"
)
async def menu_ver(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Menú",
        description="Selecciona qué deseas ver",
        color=0x2b2d31
    )

    await interaction.response.send_message(
        embed=embed,
        view=MenuPrincipalView()
    )

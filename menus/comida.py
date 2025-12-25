import discord
from discord import ui

# ================= CONFIG =================

MESEROS_ROLE_ID = 1452528262608850964
COLOR_STORE = 0x2b2d31

MENU_COMIDA = [
    {
        "nombre": "Hamburguesa Clásica",
        "emoji": "🍔",
        "descripcion": "Pan artesanal, carne jugosa, lechuga y tomate.",
        "precio": 350
    },
    {
        "nombre": "Hamburguesa Doble",
        "emoji": "🍔",
        "descripcion": "Doble carne, doble queso y salsa especial.",
        "precio": 600
    },
    {
        "nombre": "Pizza Personal",
        "emoji": "🍕",
        "descripcion": "Pizza individual de queso con orégano.",
        "precio": 450
    },
    {
        "nombre": "Hot Dog",
        "emoji": "🌭",
        "descripcion": "Salchicha premium con mostaza y kétchup.",
        "precio": 300
    },
    {
        "nombre": "Papas Fritas",
        "emoji": "🍟",
        "descripcion": "Papas crujientes con sal y especias.",
        "precio": 200
    },
    {
        "nombre": "Pollo Frito",
        "emoji": "🍗",
        "descripcion": "Piezas de pollo empanizado súper crujiente.",
        "precio": 550
    },
    {
        "nombre": "Taco Mexicano",
        "emoji": "🌮",
        "descripcion": "Taco de carne con cebolla, cilantro y limón.",
        "precio": 280
    },
    {
        "nombre": "Refresco",
        "emoji": "🥤",
        "descripcion": "Cola, naranja o limón.",
        "precio": 150
    }
]

# ================= MODAL =================

class NotaModal(ui.Modal, title="📝 Nota para el pedido"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        placeholder="Ej: sin cebolla, bien cocido, etc.",
        required=False,
        max_length=200
    )

    def __init__(self, interaction, item):
        super().__init__()
        self.interaction = interaction
        self.item = item

    async def on_submit(self, interaction: discord.Interaction):
        rol_meseros = interaction.guild.get_role(MESEROS_ROLE_ID)

        mensaje = (
            f"📢 **Nuevo pedido**\n\n"
            f"{self.item['emoji']} **Producto:** {self.item['nombre']}\n"
            f"💰 **Precio:** {self.item['precio']} monedas\n"
            f"📝 **Nota:** {self.nota.value or 'Sin nota'}\n\n"
            f"{rol_meseros.mention if rol_meseros else ''}\n"
            f"➡️ Comprar con: `/item buy {self.item['nombre']}`"
        )

        await interaction.response.send_message(
            mensaje,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

# ================= BOTÓN =================

class BotonOrdenar(ui.View):
    def __init__(self, item, balance):
        super().__init__(timeout=None)

        boton = ui.Button(
            label=str(item["precio"]),
            emoji="💵",
            style=discord.ButtonStyle.success,
            disabled=balance < item["precio"]
        )

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_modal(
                NotaModal(interaction, item)
            )

        boton.callback = callback
        self.add_item(boton)

# ================= FUNCIÓN PRINCIPAL =================

async def mostrar_menu_comida(interaction: discord.Interaction, balance: int):
    await interaction.response.defer(ephemeral=True)

    for item in MENU_COMIDA:
        embed = discord.Embed(
            title=f"{item['emoji']} {item['nombre']}",
            description=(
                f"{item['descripcion']}\n\n"
                f"💰 **{item['precio']} monedas**"
            ),
            color=COLOR_STORE
        )

        view = BotonOrdenar(item, balance)

        await interaction.followup.send(
            embed=embed,
            view=view,
            ephemeral=True
        )

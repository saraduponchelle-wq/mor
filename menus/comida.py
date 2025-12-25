import discord
from discord import ui

MESEROS_ROLE_ID = 1452528262608850964
COLOR_STORE = 0x2b2d31

MENU_COMIDA = [
    {"nombre": "Hamburguesa Clásica", "emoji": "🍔", "descripcion": "Pan artesanal, carne jugosa.", "precio": 350},
    {"nombre": "Pizza Personal", "emoji": "🍕", "descripcion": "Pizza individual de queso.", "precio": 450},
    {"nombre": "Papas Fritas", "emoji": "🍟", "descripcion": "Papas crujientes.", "precio": 200},
]

# ───────── MODAL ─────────

class NotaModal(ui.Modal, title="📝 Nota para el pedido"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        placeholder="Ej: sin cebolla",
        required=False,
        max_length=200
    )

    def __init__(self, item):
        super().__init__()
        self.item = item

    async def on_submit(self, interaction: discord.Interaction):
        rol = interaction.guild.get_role(MESEROS_ROLE_ID)

        mensaje = (
            f"📢 **Nuevo pedido**\n\n"
            f"{self.item['emoji']} **{self.item['nombre']}**\n"
            f"💰 {self.item['precio']} monedas\n"
            f"📝 {self.nota.value or 'Sin nota'}\n\n"
            f"{rol.mention if rol else ''}\n"
            f"➡️ `/item buy {self.item['nombre']}`"
        )

        await interaction.response.send_message(
            mensaje,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

# ───────── BOTÓN ─────────

class OrdenView(ui.View):
    def __init__(self, item, balance):
        super().__init__(timeout=300)

        self.add_item(
            ui.Button(
                label=f"{item['precio']} 💵",
                style=discord.ButtonStyle.success,
                disabled=balance < item["precio"],
                custom_id=item["nombre"]
            )
        )

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_modal(NotaModal(item))

        self.children[0].callback = callback

# ───────── FUNCIÓN PRINCIPAL ─────────

async def mostrar_menu_comida(ctx, balance: int):
    for item in MENU_COMIDA:
        embed = discord.Embed(
            title=f"{item['emoji']} {item['nombre']}",
            description=f"{item['descripcion']}\n\n💰 **{item['precio']} monedas**",
            color=COLOR_STORE
        )

        await ctx.send(
            embed=embed,
            view=OrdenView(item, balance)
        )

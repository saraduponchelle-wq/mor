import discord
from discord import ui, app_commands
import json

# ───────── CONFIG ─────────

MESEROS_ROLE_ID = 1452528262608850964
COLOR_STORE = 0x2b2d31
DATA_PATH = "data/bar.json"

# ───────── CARGAR JSON ─────────

def cargar_menu():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

MENU_BAR = cargar_menu()

# ───────── MODAL ─────────

class NotaBebidaModal(ui.Modal, title="🍸 Nota para la bebida"):
    nota = ui.TextInput(
        label="Nota (opcional)",
        placeholder="Ej: sin hielo, doble, etc.",
        required=False,
        max_length=200
    )

    def __init__(self, bebida):
        super().__init__()
        self.bebida = bebida

    async def on_submit(self, interaction: discord.Interaction):
        rol = interaction.guild.get_role(MESEROS_ROLE_ID)

        mensaje = (
            f"📢 **Nuevo pedido de bar**\n\n"
            f"{self.bebida['emoji']} **Bebida:** {self.bebida['nombre']}\n"
            f"💰 **Precio:** {self.bebida['precio']} monedas\n"
            f"📝 **Nota:** {self.nota.value or 'Sin nota'}\n\n"
            f"{rol.mention if rol else ''}\n"
            f"➡️ Comprar con: `/item buy {self.bebida['nombre']}`"
        )

        await interaction.response.send_message(
            mensaje,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

# ───────── SELECT ─────────

class SelectorBar(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=item["nombre"],
                description=f"{item['precio']} monedas",
                emoji=item["emoji"]
            )
            for item in MENU_BAR
        ]

        super().__init__(
            placeholder="🍹 Selecciona tu bebida",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        bebida = next(
            item for item in MENU_BAR
            if item["nombre"] == self.values[0]
        )

        await interaction.response.send_modal(
            NotaBebidaModal(bebida)
        )

# ───────── VIEW ─────────

class MenuBarView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectorBar())

# ───────── FUNCIÓN LÓGICA ─────────

async def mostrar_menu_bar(
    interaction: discord.Interaction,
    balance: int | None = None
):
    descripcion = (
        "Haz clic en una bebida para pedirla.\n"
        "El pago se realiza con `/item buy`.\n\n"
    )

    if balance is not None:
        descripcion += f"💰 **Tu balance:** {balance} monedas\n\n"

    embed = discord.Embed(
        title="🍸 Menú del Bar",
        description=descripcion,
        color=COLOR_STORE
    )

    for item in MENU_BAR:
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
        view=MenuBarView()
    )

# ───────── SLASH COMMAND /menu bar ─────────

from menus.comida import menu_group

menu_group = app_commands.Group(
    name="menu",
    description="Menús del bar"
)

@menu_group.command(
    name="bar",
    description="Muestra el menú del bar"
)
async def menu_bar(interaction: discord.Interaction):
    await mostrar_menu_bar(interaction)
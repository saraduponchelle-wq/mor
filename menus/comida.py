import discord
import json
import os

MESEROS_ROLE_ID = 123456789012345678  # ID REAL DEL ROL

DATA_PATH = "data/menu_comida.json"


def cargar_menu():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class NotaModal(discord.ui.Modal, title="📝 Nota del pedido"):
    nota = discord.ui.TextInput(
        label="Nota (opcional)",
        required=False,
        max_length=200
    )

    def __init__(self, view):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view.nota = self.nota.value or "Sin nota"
        await interaction.response.send_message(
            "✅ Nota guardada", ephemeral=True
        )


class MenuComidaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.menu = cargar_menu()
        self.producto = None
        self.nota = "Sin nota"

        opciones = [
            discord.SelectOption(
                label=nombre,
                description=f"{precio} monedas"
            )
            for nombre, precio in self.menu.items()
        ]

        self.select = discord.ui.Select(
            placeholder="🍔 Elige tu comida",
            options=opciones
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        self.producto = self.select.values[0]
        await interaction.response.send_message(
            f"✅ Seleccionaste **{self.producto}**",
            ephemeral=True
        )

    @discord.ui.button(label="📝 Añadir nota", style=discord.ButtonStyle.secondary)
    async def nota_btn(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(NotaModal(self))

    @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, button):
        if not self.producto:
            await interaction.response.send_message(
                "❌ Debes seleccionar un producto primero",
                ephemeral=True
            )
            return

        await interaction.channel.send(
            f"<@&{MESEROS_ROLE_ID}> 📢 **Nuevo pedido**\n"
            f"👤 {interaction.user.mention}\n"
            f"🍔 **Producto:** {self.producto}\n"
            f"📝 **Nota:** {self.nota}\n"
            f"🛒 **Compra:** `/item buy {self.producto}`"
        )

        await interaction.response.edit_message(
            content="✅ Pedido enviado correctamente",
            embed=None,
            view=None
        )

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, button):
        await interaction.response.edit_message(
            content="❌ Pedido cancelado",
            embed=None,
            view=None
        )


async def enviar_menu_comida(ctx):
    menu = cargar_menu()

    if not menu:
        await ctx.send("❌ El menú de comida está vacío.")
        return

    embed = discord.Embed(
        title="🍔 Menú de Comida",
        description="Selecciona un producto y confirma tu pedido",
        color=discord.Color.orange()
    )

    await ctx.send(embed=embed, view=MenuComidaView())

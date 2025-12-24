import discord
from discord.ext import commands
import json

MENU_FILE = "menus/comida.json"
MESERO_ROLE_NAME = "Meser@"
COLOR = discord.Color.orange()
TITULO = "🍔 Menú de Comida"


class MenuComidaView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.producto = None
        self.nota = None

        with open(MENU_FILE, encoding="utf-8") as f:
            self.menu = json.load(f)

        self.add_item(ProductoSelect(self.menu, self))


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return False
        return True


class ProductoSelect(discord.ui.Select):
    def __init__(self, menu: dict, parent_view: MenuComidaView):
        self.parent_view = parent_view

        options = []
        for key, data in menu.items():
            options.append(
                discord.SelectOption(
                    label=f"{data['emoji']} {data['nombre']} — {data['precio']} monedas",
                    description=data.get("descripcion", "Sin descripción"),
                    value=key
                )
            )

        super().__init__(
            placeholder="Selecciona un producto",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        key = self.values[0]
        self.parent_view.producto = self.parent_view.menu[key]

        await interaction.response.send_message(
            f"🛒 **Producto seleccionado:** "
            f"{self.parent_view.producto['emoji']} "
            f"{self.parent_view.producto['nombre']} "
            f"(**{self.parent_view.producto['precio']} monedas**)\n\n"
            "¿Qué deseas hacer?",
            view=ConfirmView(self.parent_view),
            ephemeral=True
        )


class ConfirmView(discord.ui.View):
    def __init__(self, parent_view: MenuComidaView):
        super().__init__(timeout=120)
        self.parent_view = parent_view

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, _):
        guild = interaction.guild
        rol = discord.utils.get(guild.roles, name=MESERO_ROLE_NAME)

        p = self.parent_view.producto
        nota = self.parent_view.nota or "Sin nota"

        mensaje = (
            f"🍔 **Nuevo pedido**\n"
            f"👤 Usuario: {interaction.user.mention}\n"
            f"📦 Producto: {p['emoji']} {p['nombre']}\n"
            f"📝 Nota: {nota}\n"
            f"💰 Precio: {p['precio']} monedas\n\n"
            f"👉 **Cobrar con:**\n"
            f"`/item buy {p['nombre']}`"
        )

        if rol:
            mensaje += f"\n{rol.mention}"

        await interaction.channel.send(mensaje)
        await interaction.response.send_message("✅ Pedido enviado.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Añadir nota", style=discord.ButtonStyle.secondary)
    async def añadir_nota(self, interaction: discord.Interaction, _):
        await interaction.response.send_message(
            "✍️ Escribe la nota para tu pedido:",
            ephemeral=True
        )

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            self.parent_view.nota = msg.content
            await interaction.followup.send("📝 Nota guardada.", ephemeral=True)
        except:
            await interaction.followup.send("⌛ Tiempo agotado.", ephemeral=True)

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, _):
        await interaction.response.send_message("❌ Pedido cancelado.", ephemeral=True)
        self.stop()


async def enviar_menu_comida(ctx: commands.Context):
    embed = discord.Embed(
        title=TITULO,
        description="Selecciona un producto y confirma tu pedido",
        color=COLOR
    )

    view = MenuComidaView(ctx.author.id)
    await ctx.send(embed=embed, view=view)

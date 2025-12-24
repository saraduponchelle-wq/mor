import discord
from discord.ext import commands
import json

MESERO_ROLE_NAME = "Meser@"

# ───────── VIEW PRINCIPAL ─────────

class MenuView(discord.ui.View):
    def __init__(
        self,
        *,
        author_id: int,
        menu_file: str,
        titulo: str,
        color: discord.Color,
        balance: int | None = None
    ):
        super().__init__(timeout=180)

        self.author_id = author_id
        self.balance = balance
        self.producto = None
        self.nota = None

        with open(menu_file, encoding="utf-8") as f:
            self.menu = json.load(f)

        for _, data in self.menu.items():
            precio = data["precio"]
            disabled = balance is not None and precio > balance

            self.add_item(
                ProductoButton(
                    label=f'{data["emoji"]} {data["nombre"]} — {precio}',
                    producto=data,
                    disabled=disabled,
                    parent_view=self
                )
            )

        self.embed = discord.Embed(
            title=titulo,
            description="Selecciona un producto",
            color=color
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return False
        return True

# ───────── BOTÓN DE PRODUCTO ─────────

class ProductoButton(discord.ui.Button):
    def __init__(self, *, label, producto, disabled, parent_view):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.success,
            disabled=disabled
        )
        self.producto = producto
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.producto = self.producto

        await interaction.response.send_message(
            f"🛒 **Producto seleccionado:** {self.producto['emoji']} {self.producto['nombre']}\n"
            "Elige una opción:",
            view=ConfirmView(self.parent_view),
            ephemeral=True
        )

# ───────── VIEW DE CONFIRMACIÓN ─────────

class ConfirmView(discord.ui.View):
    def __init__(self, parent_view: MenuView):
        super().__init__(timeout=120)
        self.parent_view = parent_view

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, _):
        guild = interaction.guild
        rol = discord.utils.get(guild.roles, name=MESERO_ROLE_NAME)

        producto = self.parent_view.producto
        nota = self.parent_view.nota or "Sin nota"

        mensaje = (
            f"🧾 **Nuevo pedido**\n"
            f"👤 Usuario: {interaction.user.mention}\n"
            f"📦 Producto: {producto['emoji']} {producto['nombre']}\n"
            f"📝 Nota: {nota}\n"
            f"💰 Precio: {producto['precio']}\n\n"
            f"👉 **Comando para pagar:**\n"
            f"`/item buy {producto['nombre']}`\n"
        )

        if rol:
            mensaje += f"\n{rol.mention}"

        await interaction.channel.send(mensaje)
        await interaction.response.send_message(
            "✅ Pedido enviado a los meseros.",
            ephemeral=True
        )
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
            await interaction.followup.send(
                "⌛ Tiempo agotado. No se guardó la nota.",
                ephemeral=True
            )

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, _):
        await interaction.response.send_message(
            "❌ Pedido cancelado.",
            ephemeral=True
        )
        self.stop()

# ───────── FUNCIÓN PARA USAR EN COGS ─────────

async def enviar_menu(
    ctx: commands.Context,
    *,
    menu_file: str,
    titulo: str,
    color: discord.Color,
    balance: int | None = None
):
    view = MenuView(
        author_id=ctx.author.id,
        menu_file=menu_file,
        titulo=titulo,
        color=color,
        balance=balance
    )

    await ctx.send(embed=view.embed, view=view)

import discord
from discord.ext import commands
import json

MESERO_ROLE_NAME = "Meser@"
MENU_FILE = "menus/bar.json"
COLOR = discord.Color.dark_red()
TITULO = "🍸 Carta del Bar"


class MenuView(discord.ui.View):
    def __init__(self, author_id, menu, balance=None):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.menu = menu
        self.balance = balance
        self.producto = None
        self.nota = None

        for key, data in menu.items():
            precio = data["precio"]
            disabled = balance is not None and precio > balance

            self.add_item(
                ProductoButton(
                    label=f'{data["emoji"]} {data["nombre"]} — {precio}',
                    producto=data,
                    disabled=disabled,
                    view=self
                )
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.", ephemeral=True
            )
            return False
        return True


class ProductoButton(discord.ui.Button):
    def __init__(self, label, producto, disabled, view):
        super().__init__(style=discord.ButtonStyle.success, label=label, disabled=disabled)
        self.producto = producto
        self.menu_view = view

    async def callback(self, interaction: discord.Interaction):
        self.menu_view.producto = self.producto
        await interaction.response.send_message(
            f"Has seleccionado **{self.producto['nombre']}**.\n"
            "Usa los botones para confirmar, cancelar o añadir nota.",
            view=ConfirmView(self.menu_view),
            ephemeral=True
        )


class ConfirmView(discord.ui.View):
    def __init__(self, menu_view):
        super().__init__(timeout=120)
        self.menu_view = menu_view

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, _):
        guild = interaction.guild
        rol = discord.utils.get(guild.roles, name=MESERO_ROLE_NAME)

        p = self.menu_view.producto
        nota = self.menu_view.nota or "Sin nota"

        mensaje = (
            f"🍸 **Nuevo pedido**\n"
            f"👤 Usuario: {interaction.user.mention}\n"
            f"📦 Producto: {p['emoji']} {p['nombre']}\n"
            f"📝 Nota: {nota}\n"
            f"💰 Precio: {p['precio']}\n\n"
            f"👉 **Comando para cobrar:**\n"
            f"`/item buy {p['nombre']}`\n"
        )

        if rol:
            mensaje += rol.mention

        await interaction.channel.send(mensaje)
        await interaction.response.send_message("✅ Pedido enviado.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Añadir nota", style=discord.ButtonStyle.secondary)
    async def nota(self, interaction: discord.Interaction, _):
        await interaction.response.send_message(
            "✍️ Escribe la nota para tu pedido:",
            ephemeral=True
        )

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        msg = await interaction.client.wait_for("message", check=check, timeout=60)
        self.menu_view.nota = msg.content
        await interaction.followup.send("📝 Nota guardada.", ephemeral=True)

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, _):
        await interaction.response.send_message("❌ Pedido cancelado.", ephemeral=True)
        self.stop()


class MenuBar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menubar(self, ctx, balance: int = None):
        with open(MENU_FILE, encoding="utf-8") as f:
            menu = json.load(f)

        embed = discord.Embed(
            title=TITULO,
            description="Selecciona una bebida del bar",
            color=COLOR
        )

        view = MenuView(ctx.author.id, menu, balance)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(MenuBar(bot))

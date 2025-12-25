import discord
import json

RUTA_MENU_COMIDA = "menus/comida.json"
ROL_MESERO = "Mesero"


# ───────── MODAL NOTA ─────────

class NotaModal(discord.ui.Modal, title="📝 Nota del pedido"):
    nota = discord.ui.TextInput(
        label="Nota",
        placeholder="Ej: Sin cebolla, poco hielo, para llevar...",
        required=False,
        max_length=200
    )

    def __init__(self, view):
        super().__init__()
        self.view_menu = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view_menu.nota = self.nota.value or "Sin nota."
        await interaction.response.send_message(
            "✅ Nota añadida correctamente.",
            ephemeral=True
        )


# ───────── BOTONES ─────────

class ProductoButton(discord.ui.Button):
    def __init__(self, item, puede_pagar, view):
        super().__init__(
            label=f'{item["nombre"]} — {item["precio"]}',
            style=discord.ButtonStyle.success if puede_pagar else discord.ButtonStyle.secondary,
            disabled=not puede_pagar
        )
        self.item = item
        self.menu_view = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.menu_view.usuario.id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return

        guild = interaction.guild
        rol_mesero = discord.utils.get(guild.roles, name=ROL_MESERO)

        texto = (
            f"🍽️ **NUEVO PEDIDO**\n\n"
            f"👤 Usuario: {interaction.user.mention}\n"
            f"📦 Producto: **{self.item['nombre']}**\n"
            f"💰 Precio: **{self.item['precio']} monedas**\n"
            f"📝 Nota: {self.menu_view.nota}\n\n"
            f"💳 **Comando para pagar:**\n"
            f"`/item buy {self.item['nombre']}`"
        )

        await interaction.response.send_message(
            texto,
            allowed_mentions=discord.AllowedMentions(roles=True, users=True)
        )

        if rol_mesero:
            await interaction.followup.send(
                rol_mesero.mention,
                allowed_mentions=discord.AllowedMentions(roles=True)
            )

        self.menu_view.stop()


class NotaButton(discord.ui.Button):
    def __init__(self, view):
        super().__init__(
            label="📝 Añadir nota",
            style=discord.ButtonStyle.primary
        )
        self.menu_view = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.menu_view.usuario.id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            NotaModal(self.menu_view)
        )


class CancelarButton(discord.ui.Button):
    def __init__(self, view):
        super().__init__(
            label="❌ Cancelar",
            style=discord.ButtonStyle.danger
        )
        self.menu_view = view

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.menu_view.usuario.id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.",
                ephemeral=True
            )
            return

        await interaction.response.edit_message(
            content="❌ Pedido cancelado.",
            embed=None,
            view=None
        )
        self.menu_view.stop()


# ───────── VIEW DEL MENÚ ─────────

class MenuComidaView(discord.ui.View):
    def __init__(self, ctx, menu, balance):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.usuario = ctx.author
        self.menu = menu
        self.balance = balance
        self.nota = "Sin nota."

        for item in menu.values():
            puede_pagar = balance is None or balance >= item["precio"]
            self.add_item(
                ProductoButton(item, puede_pagar, self)
            )

        self.add_item(NotaButton(self))
        self.add_item(CancelarButton(self))


# ───────── FUNCIÓN PÚBLICA (SE LLAMA DESDE MAIN) ─────────

async def mostrar_menu_comida(ctx, balance=None):
    with open(RUTA_MENU_COMIDA, encoding="utf-8") as f:
        menu = json.load(f)

    embed = discord.Embed(
        title="🍔 Menú de Comida",
        description=(
            "Haz click en un producto para pedirlo.\n"
            "El pago se realiza con `/item buy`."
        ),
        color=discord.Color.orange()
    )

    if balance is not None:
        embed.add_field(
            name="💰 Tus monedas",
            value=str(balance),
            inline=False
        )

    embed.add_field(
        name="━━━━━━━━━━━━━━━━━━━━",
        value="\u200b",
        inline=False
    )

    for item in menu.values():
        embed.add_field(
            name=item["nombre"],
            value=(
                f'{item["descripcion"]}\n'
                f'💰 **{item["precio']} monedas**'
            ),
            inline=False
        )

    view = MenuComidaView(ctx, menu, balance)
    await ctx.send(embed=embed, view=view)

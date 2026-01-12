# comands/salonp/__init__.py
from discord import app_commands

# Importa los comandos
from .salonp_commands import salonp_create, salonp_invite, salonp_eliminate

# Crear grupo "salonp" (todo en minúsculas)
salonp_group = app_commands.Group(
    name="salonp",
    description="Comandos de salones privados"
)

# Añadir comandos al grupo
salonp_group.add_command(salonp_create)
salonp_group.add_command(salonp_invite)
salonp_group.add_command(salonp_eliminate)

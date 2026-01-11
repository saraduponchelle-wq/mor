# comands/salonp/__init__.py

from discord import app_commands
from .create import salonp_create
from .invite import salonp_invite
from .eliminate import salonp_eliminate

# GRUPO DE COMANDOS
salonp_group = app_commands.Group(
    name="salonp",  # <-- todo en minúsculas
    description="Comandos para crear y manejar salones privados"
)

# Agregamos los comandos al grupo
salonp_group.add_command(salonp_create)
salonp_group.add_command(salonp_invite)
salonp_group.add_command(salonp_eliminate)

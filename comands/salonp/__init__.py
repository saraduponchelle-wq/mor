
from .create import create_command
from .invite import invite_command
from .eliminate import eliminate_command
from discord import app_commands

# Grupo de comandos
salonp_group = app_commands.Group(
    name="salonP",
    description="Gestiona tus chats privados del foro"
)

# Añadir comandos
salonp_group.add_command(create_command)
salonp_group.add_command(invite_command)
salonp_group.add_command(eliminate_command)

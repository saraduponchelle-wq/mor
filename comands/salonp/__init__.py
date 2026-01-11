from discord import app_commands

salonp_group = app_commands.Group(
    name="salonp",
    description="Salones privados"
)

from .create import *
from .invite import *
from .eliminate import *

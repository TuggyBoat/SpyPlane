from discord import app_commands, Intents, Client

from spyplane.constants import GUILD_ID


class SpyPlane(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents, application_id=GUILD_ID)
        self.tree = app_commands.CommandTree(self)


bot = SpyPlane(intents=Intents.default())



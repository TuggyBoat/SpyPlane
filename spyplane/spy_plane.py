from discord import app_commands, Intents, Client, Object

from spyplane.constants import GUILD_ID, APPLICATION_ID


class SpyPlane(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents, application_id=APPLICATION_ID)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        discord_server_object = Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=discord_server_object)
        await self.tree.sync(guild=discord_server_object)
        print('commands synced')


bot = SpyPlane(intents=Intents.default())

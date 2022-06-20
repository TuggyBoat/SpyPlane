from asyncio import Lock
from threading import Thread
from typing import Optional, Union

import aiosqlite
from aiosqlite import Connection
from discord import app_commands, Intents, Client, Object, Emoji
from discord.abc import GuildChannel, PrivateChannel

from spyplane.constants import GUILD_ID, APPLICATION_ID, DB_PATH


class SpyPlane(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents, application_id=APPLICATION_ID)
        self.db: Optional[Connection] = None
        self.tree = app_commands.CommandTree(self)
        self.lock: Optional[Lock] = None
        self.emoji_bullseye: Optional[Emoji] = None
        self.channel: Optional[Union[GuildChannel, Thread, PrivateChannel]] = None

    async def setup_hook(self):
        discord_server_object = Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=discord_server_object)
        await self.tree.sync(guild=discord_server_object)
        print('commands synced')
        await self.dbinit()

    async def dbinit(self):
        self.db = await aiosqlite.connect(DB_PATH)
        await self.db.set_trace_callback(print)
        print('db open')

    async def close(self):
        await self.dbclose()
        await super().close()  # Important! This will log the bot out.

    async def dbclose(self):
        print('closing DB connection')
        await self.db.close()


bot = SpyPlane(intents=Intents.default())

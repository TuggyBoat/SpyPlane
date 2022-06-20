import asyncio

import discord

from spyplane.constants import CONTROL_CHANNEL
from spyplane.database.config_repository import ConfigRepository
from spyplane.services.sync_service import SyncService
from spyplane.services.systems_posting_service import SystemsPostingService
from spyplane.spy_plane import bot


class PostAfterTickService:
    def __init__(self, sheets=SystemsPostingService(), sync=SyncService(), repo=ConfigRepository()):
        self.sheets = sheets
        self.repo = repo
        self.sync = sync

    async def run_after_interval(self):
        hours = await ConfigRepository().get_config("interval_hours")
        channel = bot.get_channel(CONTROL_CHANNEL)
        await channel.send(f"Tick detected. Spy Plane will take off in ~ {hours.value} hours")
        seconds = int(hours.value) * 60
        print(f"Waiting for {seconds} seconds")
        await asyncio.sleep(seconds)
        print(f"Synchronizing with google sheets")
        await self.sync.sync_db_sheet()
        print(f"Posting systems now")
        await SystemsPostingService(channel).publish_systems_to_scout()

    async def validate_message(self, message: discord.message.Message):
        # if 'Tick Detected' not in message and 'Latest Tick At' not in message:
        #     print("'Tick Detected' and 'Latest Tick At' is not in message")
        #     return
        print('Tick detection message found!')
        asyncio.create_task(self.run_after_interval())

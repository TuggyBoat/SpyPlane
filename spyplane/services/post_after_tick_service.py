import asyncio

import discord

from spyplane.constants import log
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
        try:
            hours = await ConfigRepository().get_config("interval_hours")
            await bot.channel.send(f"Tick detected. Spy Plane will take off in ~ {hours.value} hours")
            seconds = int(hours.value) * 3600
            log(f"Waiting for {seconds} seconds")
            await asyncio.sleep(seconds)
            log("Synchronizing with google sheets")
            await self.sync.sync_db_sheet()
            log("Posting systems now")
            await SystemsPostingService().publish_systems_to_scout()
        except Exception as e:
            log("Exception when running after interval")
            log(str(e))

    async def validate_message(self, message: discord.message.Message):
        message_to = 'Tick Detected' not in message.content or 'Latest Tick At' not in message.content
        print(f"Condition: {message_to}", flush=True)
        log('Tick detection message found!')
        asyncio.create_task(self.run_after_interval())

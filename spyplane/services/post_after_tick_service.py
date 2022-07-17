import asyncio

import discord

from spyplane.constants import log, log_exception, BGS_BOT_USER_ID, TICK_CHANNEL
from spyplane.database.config_repository import ConfigRepository
from spyplane.services.sync_service import SyncService
from spyplane.services.systems_posting_service import SystemsPostingService
from spyplane.services.tick_service import TickService
from spyplane.spy_plane import bot


class PostAfterTickService:
    def __init__(self, sheets=SystemsPostingService(), sync=SyncService(), repo=ConfigRepository(), ticks=TickService()):
        self.sheets = sheets
        self.repo = repo
        self.sync = sync
        self.tick_service = ticks

    async def run_after_interval(self):
        try:
            hours = await ConfigRepository().get_config("interval_hours")
            message = f"Tick detected. Spy Plane will take off in ~ {hours.value} hours"
            log(message)
            await bot.channel.send(message)
            seconds = int(hours.value) * 3600
            log(f"Waiting for {seconds} seconds")
            await asyncio.sleep(seconds)
            log("Synchronizing with google sheets")
            await self.sync.sync_db_sheet()
            log("Posting systems now")
            await SystemsPostingService().publish_systems_to_scout()
        except Exception as e:
            log_exception("run_after_interval", e)

    async def tick_check_and_schedule(self):
        """
        This is meant to be called in an aiocron. Uses :py:class:`~spyplane.services.TickService`
        :return:
        """
        has_ticked = await self.tick_service.has_ticked()
        if has_ticked:
            asyncio.create_task(self.run_after_interval())

    async def validate_and_schedule(self, message: discord.message.Message):
        if message.author.id!=BGS_BOT_USER_ID or message.channel.id!=TICK_CHANNEL:
            return
        log("Message from BGS Bot in tick channel!")
        if not len(message.embeds) or not len(message.embeds[0].fields):
            log("Not the tick message. Embeds missing")
            return
        if message.embeds[0].fields[0].name!="Latest Tick At" or message.embeds[0].title!="Tick Detected":
            log(f"Not the tick message. Field name: {message.embeds[0].fields[0].name} Title: {message.embeds[0].title}")
            return
        log('Tick detection message found!')
        asyncio.create_task(self.run_after_interval())

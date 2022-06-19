import discord
from discord.ext import commands

from spyplane.constants import BGS_BOT_USER_ID, CONTROL_CHANNEL
from spyplane.database.config_repository import ConfigRepository
from spyplane.spy_plane import bot


class TickDetection(commands.Cog):

    def __init__(self):
        self.repo = ConfigRepository()

    async def validate_message(self, message: discord.message.Message):
        if message.author.id!=BGS_BOT_USER_ID:
            return
        if 'Tick Detected' not in message and 'Latest Tick At' not in message:
            return
        print('Tick detection message found!')
        hours = await self.repo.get_config("interval_hours")
        await bot.get_channel(CONTROL_CHANNEL).send(f"Tick detected. Spy Plane will take off in ~ {hours.value} hours")

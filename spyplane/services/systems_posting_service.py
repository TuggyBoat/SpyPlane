import aiosqlite
import discord.message
from discord import MessageType

from spyplane.constants import EMOJI_BULLSEYE, DB_PATH
from spyplane.database.systems_repository import SystemsRepository
from spyplane.spy_plane import bot


class SystemsPostingService:

    def __init__(self, channel):
        self.channel = channel

    async def publish_systems_to_scout(self):
        repo = SystemsRepository()
        async with aiosqlite.connect(DB_PATH) as db:
            await repo.init(db)
            valid_systems = await repo.get_valid_systems()
        emoji_bullseye = bot.get_emoji(EMOJI_BULLSEYE)
        await self.channel.purge(check=self.is_not_pinned_message)
        for scout_system in valid_systems:
            message = await self.channel.send(scout_system.system)
            await message.add_reaction('✅' if emoji_bullseye is None else emoji_bullseye)

    @staticmethod
    def is_not_pinned_message(message: discord.message.Message) -> bool:
        return not message.pinned and message.type!=MessageType.chat_input_command

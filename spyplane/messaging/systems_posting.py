from typing import List

import discord.message

from spyplane.constants import EMOJI_BULLSEYE
from spyplane.sheets.scout_system import ScoutSystem
from spyplane.spy_plane import bot


class SystemsPosting:

    def __init__(self, channel):
        self.channel = channel

    async def publish_systems_to_scout(self, scout_list: List[ScoutSystem]):
        emoji_bullseye = bot.get_emoji(EMOJI_BULLSEYE)
        await self.channel.purge(check=self.is_not_pinned_message)
        for scout_system in scout_list:
            message = await self.channel.send(scout_system.system)
            await message.add_reaction('✅' if emoji_bullseye is None else emoji_bullseye)

    @staticmethod
    def is_not_pinned_message(message: discord.message.Message) -> bool:
        return not message.pinned

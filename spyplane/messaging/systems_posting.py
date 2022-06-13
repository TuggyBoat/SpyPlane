from typing import List

from spyplane.constants import EMOJI_BULLSEYE
from spyplane.sheets.scout_system import ScoutSystem
from spyplane.spy_plane import bot



class SystemsPosting:

    def __init__(self, channel):
        self.channel = channel

    async def publish_systems_to_scout(self, list: List[ScoutSystem]):
        emoji_bullseye = bot.get_emoji(EMOJI_BULLSEYE)
        for scout_system in list:
            message = await self.channel.send(scout_system.system)
            await message.add_reaction('✅' if emoji_bullseye is None else emoji_bullseye)

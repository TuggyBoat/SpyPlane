from typing import List

import discord

from spyplane.sheets.scout_system import ScoutSystem
from spyplane.spy_plane import bot

emoji_100 = 971408439035174962
emoji_kappa = 985603214051262545
emoji_bullseye_id = 98418768978183374


class SystemsPosting:

    def __init__(self, channel: discord.abc.Messageable):
        self.channel = channel

    async def publish_systems_to_scout(self, list: List[ScoutSystem]):
        for scout_system in list:
            message = await self.channel.send(scout_system.system)
            emoji_bullseye = bot.get_emoji(emoji_bullseye_id)
            await message.add_reaction(emoji_bullseye)

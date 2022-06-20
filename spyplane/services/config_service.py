import time
from datetime import datetime

import discord
from discord import Color, Embed

from spyplane.database.config_repository import ConfigRepository


class ConfigService:
    def __init__(self, repo=ConfigRepository()):
        self.repo = repo


    async def dump_config_embed(self) -> Embed:
        embed = ConfigService.common_embed_setup(None, 'Configuration')
        config_dump = await self.repo.dump_config()
        for config in config_dump:
            embed.add_field(name=config.name, value=config.value, inline=False)
        return embed

    @staticmethod
    def common_embed_setup(description, title):
        embed = discord.Embed(
            title=title,
            description=description,
            color=Color.dark_purple(),
            timestamp=datetime.utcfromtimestamp(time.time())
        )
        embed.set_footer(icon_url='https://edassets.org/static/img/pilots-federation/explorer/rank-9.png', text='P.T.N. Spy Plane ™')
        return embed

import time
from datetime import datetime

import discord
from discord import Color, Embed

from spyplane.database.config_repository import ConfigRepository
from spyplane.database.systems_repository import SystemsRepository


class ConfigService:
    def __init__(self, repo=ConfigRepository(), system_repo=SystemsRepository()):
        self.repo = repo
        self.system_repo = system_repo


    async def dump_config_embed(self) -> Embed:
        embed = ConfigService.common_embed_setup(None, 'Configuration')
        config_dump = await self.repo.dump_config()
        for config in config_dump:
            embed.add_field(name=config.name, value=config.value, inline=False)
        return embed

    async def update_config(self, name, value):
        message_addon = ""
        await self.repo.update_config(name, value)
        if name=="carryover" and value not in ["true", "True", "yes", "Yes"]:
            await self.system_repo.purge_posted_systems()
            message_addon = " Also removed current carryover systems, if any"
        return message_addon

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

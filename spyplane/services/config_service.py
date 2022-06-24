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

    async def update_config(self, name: str, value: str):
        # TODO refactor when we have more configuration
        name_lower = name.lower()
        value_lower = value.lower()
        supported_configs = ["carryover", "interval_hours"]
        if name_lower not in supported_configs:
            return f"Config was not set. We support only {supported_configs}"
        supported_carryover = ["true", "false"]
        if name_lower=="carryover" and value_lower not in supported_carryover:
            return f"Config was not set. carryover supports only {supported_carryover}"
        if name_lower=="interval_hours" and (not value_lower.isdigit() or int(value_lower) < 1 or int(value_lower) > 24):
            return f"Config was not set. interval_hours supports only numbers between 1 and 24"

        await self.repo.update_config(name_lower, value_lower)
        message = f"Config {name_lower} was set to {value_lower}"
        if name_lower=="carryover" and value_lower=="false":
            await self.system_repo.purge_posted_systems()
            message = f"Config {name_lower} was set to {value_lower}. Also removed current carryover systems, if any"
        return message

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

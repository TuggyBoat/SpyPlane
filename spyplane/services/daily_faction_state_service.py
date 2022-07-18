import asyncio
import time
from typing import List
from datetime import datetime

import discord
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.system_state import FactionState
from spyplane.services.ebgs_service import EliteBgsService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper


class DailyFactionStateService:
    def __init__(
        self,
        sheets=SpreadsheetHelper(),
        repo=SystemsRepository(),
        ebgs=EliteBgsService(),
    ):
        self.sheets: SpreadsheetHelper = sheets
        self.repo: SystemsRepository = repo
        self.ebgs: EliteBgsService = ebgs

    async def notify_daily_news(self, channel):
        embed = self.common_embed_setup("Trending systems!", "Spy Plane")
        systems = self.sheets.read_daily_sheet()
        valid_systems = [
            system for system in systems if await self.repo.is_valid_system(system)
        ]  # Select N+1 issue, but we can tolerate this for a while!
        
        tasks = [self.ebgs_task(system, embed) for system in valid_systems]
        await asyncio.gather(*tasks)
        await channel.send(embed=embed)
    
    async def ebgs_task(self, system, embed):
        faction_states_list = await self.ebgs.get_system_faction_not_none_states(system)
        if len(faction_states_list):
            embed.add_field(name=system, value=self.combine(faction_states_list), inline=False)

    @staticmethod
    def combine(faction_states_list: List[FactionState]) -> str:
        return "\n".join([faction_state.short_form() for faction_state in faction_states_list])

    @staticmethod
    def common_embed_setup(description, title):
        embed = discord.Embed(
            title=title,
            url="https://inara.cz/",
            description=description,
            color=discord.Color.brand_red(),
            timestamp=datetime.utcfromtimestamp(time.time()),
        )
        embed.set_footer(
            icon_url="https://edassets.org/static/img/companies/GalNet.png",
            text="P.T.N. Faction News ™",
        )
        return embed

import asyncio
import time
from typing import List
from datetime import datetime

import discord
from spyplane.constants import log_exception
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.system_state import FactionState
from spyplane.services.ebgs_service import EliteBgsService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper
from spyplane.spy_plane import bot


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

    async def notify_daily_news(self, channel = None):
        embed = self.common_embed_setup("None", "Factions Expanding")
        systems = self.sheets.read_daily_sheet()
        valid_systems = [
            system for system in systems if await self.repo.is_valid_system(system)
        ]  # Select N+1 issue, but we can tolerate this for a while!
        factions_in_expansion = []
        tasks = [self.ebgs_task(system, embed, factions_in_expansion) for system in valid_systems]
        await asyncio.gather(*tasks)
        if len(factions_in_expansion):
            embed.description = "\n".join(set(factions_in_expansion))[0:4096]
        await (channel or bot.report_channel).send(embed=embed)
    
    async def ebgs_task(self, system, embed, factions_in_expansion: List[str]):
        try:
            faction_states_list = await self.ebgs.get_system_faction_not_none_states(system)
            faction_states_sans_expansion = [faction_state for faction_state in faction_states_list if not faction_state.is_just_expansion()]
            if len(faction_states_sans_expansion):
                embed.add_field(name=system, value=self.combine(faction_states_sans_expansion), inline=False)
            for faction_state in faction_states_list:
                if faction_state.is_just_expansion():
                    suffix = " (Pending)" if faction_state.is_expansion_pending() else " (Active)"
                    factions_in_expansion.append(faction_state.name + suffix) 
        except Exception as e:
            log_exception("ebgs_task for " + system, e)

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

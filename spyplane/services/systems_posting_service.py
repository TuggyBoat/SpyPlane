import datetime
from typing import List, Dict, cast

import discord.message

from spyplane.constants import FACTION_SCOUT_ROLE_ID
from spyplane.database.config_repository import ConfigRepository
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.scout_system import ScoutSystem
from spyplane.spy_plane import bot


class SystemsPostingService:

    def __init__(self, repo=SystemsRepository(), config_repo=ConfigRepository()):
        self.repo = repo
        self.config_repo = config_repo
        self.start_date = datetime.date(2022, 6, 18)  # start day randomly chosen for the daily sequence

    async def publish_systems_to_scout(self):
        valid_systems = await self.repo.get_valid_systems()
        should_carryover = (await self.config_repo.get_config("carryover")).value.lower() in ["true", "yes", "y", "t"]
        carryover = []
        if should_carryover:
            carryover = await self.repo.get_carryover_systems()
        await bot.channel.purge(check=self.is_not_pinned_message)
        splits = self.split_valid_systems(valid_systems, (datetime.date.today() - self.start_date).days, carryover)
        await self.post_list(splits, 'Primary')
        await self.post_list(splits, 'Secondary')
        await self.post_list(splits, 'Tertiary')
        if len(valid_systems):
            await bot.channel.send(f"<@&{FACTION_SCOUT_ROLE_ID}> List Updated")

    async def post_list(self, splits, priority_string):
        if len(splits[priority_string]):
            if priority_string!='Primary':
                await bot.channel.send(f"__**{priority_string} List**__")
                await self.repo.begin()
                await self.repo.write_system_to_post(splits[priority_string])
                await self.repo.commit()
        for scout_system in splits[priority_string]:
            message = await bot.channel.send(scout_system.system)
            await message.add_reaction(bot.emoji_bullseye)
        else:
            print(f'Empty {priority_string} List')

    @staticmethod
    def is_not_pinned_message(message: discord.message.Message) -> bool:
        return not message.pinned


    def split_valid_systems(self, systems: List[ScoutSystem], daily_sequence: int, carryover: List[ScoutSystem]) -> Dict[str, List[ScoutSystem]]:
        splits = {
            'Primary': [s for s in systems if int(s.priority)==1],
            'Secondary': [s for s in systems if int(s.priority)==2],
            'Tertiary': [s for s in systems if int(s.priority) > 2]
        }
        every_other_day = list(self.split(splits['Secondary'], 2))
        every_third_day = list(self.split(splits['Tertiary'], 3))
        secondary_today: List[ScoutSystem] = cast(List[ScoutSystem], every_other_day[daily_sequence % 2])
        tertiary_today: List[ScoutSystem] = cast(List[ScoutSystem], every_third_day[daily_sequence % 3])
        return {
            'Primary': splits['Primary'],
            'Secondary': secondary_today + [s for s in carryover if int(s.priority)==2 and s.system not in [l.system for l in secondary_today]],
            'Tertiary': tertiary_today + [s for s in carryover if int(s.priority) > 2 and s.system not in [l.system for l in tertiary_today]]
        }


    @staticmethod  # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    def split(array, split_size):
        k, m = divmod(len(array), split_size)
        return (array[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(split_size))

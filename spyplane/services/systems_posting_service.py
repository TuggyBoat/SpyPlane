import datetime
from typing import List, Dict, cast

import aiosqlite
import discord.message

from spyplane.constants import EMOJI_BULLSEYE, DB_PATH, FACTION_SCOUT_ROLE_ID
from spyplane.database.systems_repository import SystemsRepository
from spyplane.sheets.scout_system import ScoutSystem
from spyplane.spy_plane import bot


class SystemsPostingService:

    def __init__(self, channel):
        self.channel = channel

    start_date = datetime.date(2022, 6, 18)  # start day randomly chosen for the daily sequence

    async def publish_systems_to_scout(self):
        repo = SystemsRepository()
        async with aiosqlite.connect(DB_PATH) as db:
            await repo.init(db)
            valid_systems = await repo.get_valid_systems()
        emoji_bullseye = bot.get_emoji(EMOJI_BULLSEYE)
        await self.channel.purge(check=is_not_pinned_message)
        splits = split_valid_systems(valid_systems, (datetime.date.today() - self.start_date).days)
        await self.post_list(emoji_bullseye, splits, 'Primary')
        await self.post_list(emoji_bullseye, splits, 'Secondary')
        await self.post_list(emoji_bullseye, splits, 'Tertiary')
        await self.channel.send(f"<@&{FACTION_SCOUT_ROLE_ID}> List Updated")

    async def post_list(self, emoji_bullseye, splits, priority_string):
        if len(splits[priority_string]):
            if priority_string!='Primary':
                await self.channel.send(f"__**{priority_string} List**__")
            for scout_system in splits[priority_string]:
                message = await self.channel.send(scout_system.system)
                await message.add_reaction('✅' if emoji_bullseye is None else emoji_bullseye)
        else:
            print(f'Empty {priority_string} List')


def is_not_pinned_message(message: discord.message.Message) -> bool:
    return not message.pinned


def split_valid_systems(systems: List[ScoutSystem], daily_sequence: int) -> Dict[str, List[ScoutSystem]]:
    # TODO: use a db sequence instead of day of week.
    splits = {
        'Primary': [s for s in systems if int(s.priority)==1],
        'Secondary': [s for s in systems if int(s.priority)==2],
        'Tertiary': [s for s in systems if int(s.priority) > 2]
    }
    every_other_day = list(split(splits['Secondary'], 2))
    every_third_day = list(split(splits['Tertiary'], 3))
    return {
        'Primary': splits['Primary'],
        'Secondary': cast(List[ScoutSystem], every_other_day[daily_sequence % 2]),
        'Tertiary': cast(List[ScoutSystem], every_third_day[daily_sequence % 3])
    }


def split(a, n):  # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

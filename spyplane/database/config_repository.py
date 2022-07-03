import time
from datetime import datetime
from typing import List

from spyplane.database.base_repository import BaseRepository
from spyplane.models.config import Config

update_config = '''
update configuration
set value=?, timestamp=?
where name=?;
'''
get_config = '''
select *
from configuration
where name = ?;
'''
dump_config = '''
select *
from configuration
'''


class ConfigRepository(BaseRepository):

    async def get_config(self, name) -> Config:
        async with self.db().execute(get_config, [name]) as cur:
            row = await cur.fetchone()
        return Config(row[0], row[1], row[2], datetime.utcfromtimestamp(row[3]))

    async def dump_config(self) -> List[Config]:
        async with self.db().execute(dump_config) as cur:
            rows = await cur.fetchall()
        return [Config(row[0], row[1], row[2], datetime.utcfromtimestamp(row[3])) for row in rows]

    async def update_config(self, name: str, value: str):
        await self.begin()
        await self.db().execute(update_config, (value, time.mktime(datetime.now().timetuple()), name))
        await self.commit()

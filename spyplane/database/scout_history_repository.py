import time
from datetime import datetime
from typing import Optional

from spyplane.database.base_repository import BaseRepository
from spyplane.models.scout_history import ScoutHistory
from spyplane.models.scout_system import ScoutSystem

insert_scout_history = '''
insert into scout_history (system_name, username, userid, timestamp) values (?,?,?,?);
'''

read_scout_history = '''
select id, system_name, username, userid, timestamp from scout_history where 1=1
'''

purge_scout_history = '''
delete from scout_history
'''


class ScoutHistoryRepository(BaseRepository):

    async def record_scout(self, system: ScoutSystem, username, userid, ts=datetime.now()):
        await self.db().execute(insert_scout_history, (system.system, username, userid, time.mktime(ts.timetuple())))
        print(f"Added history: {system.system}, {username}, {userid}, {ts}")

    async def get_history(self, system: Optional[str] = None, username: Optional[str] = None, userid: Optional[int] = None):
        params = []
        query = read_scout_history
        if system is not None:
            query += ' and system_name=?'
            params.append(system)
        if username is not None:
            query += ' and username=?'
            params.append(username)
        if userid is not None:
            query += ' and userid=?'
            params.append(userid)
        async with self.db().execute(query, parameters=params) as cur:
            rows = await cur.fetchall()
            return [ScoutHistory(r[0], r[1], r[2], r[3], datetime.utcfromtimestamp(r[4])) for r in rows]

    async def purge_scout_systems_history(self) -> None:
        await self.db().execute(purge_scout_history)

from typing import List

from aiosqlite import Connection

from spyplane.models.scout_system import ScoutSystem

insert_scout_system = '''
insert into scout_systems (system_name, priority, rownum) values (?,?,?);
'''
select_scout_system = '''
select *
from scout_systems
where system_name = ?;
'''

get_valid_systems_query = '''
select s.system_name, s.priority, s.rownum ō
from scout_systems s
join systems m on s.system_name = m.name
where s.priority != '' and printf("%d", s.priority) = s.priority
'''

purge_scout_table = '''
delete from scout_systems
'''

get_invalid_systems_query = '''
select ss.system_name, ss.priority, ss.rownum
from scout_systems ss
left join (
%s
) m on ss.system_name = m.system_name
where m.system_name is null;
'''


class SystemsRepository:

    def __init__(self):
        self.db = None

    async def init(self, db: Connection):
        await db.set_trace_callback(print)
        self.db = db

    async def get_invalid_systems(self) -> List[ScoutSystem]:
        return await self.get_systems(get_invalid_systems_query % get_valid_systems_query)

    async def get_valid_systems(self) -> List[ScoutSystem]:
        return await self.get_systems(get_valid_systems_query)

    async def get_system(self, system_name) -> ScoutSystem:
        async with self.db.execute(select_scout_system, [system_name]) as cur:
            row = await cur.fetchone()
        return ScoutSystem(row[0], row[1], row[2])

    async def get_systems(self, query) -> List[ScoutSystem]:
        async with self.db.execute(query) as cur:
            rows = await cur.fetchall()
        return [ScoutSystem(row[0], row[1], row[2]) for row in rows]

    async def write_system_to_scout(self, systems_to_scout: List[ScoutSystem], commit=True):
        await self.db.execute("BEGIN")
        async with self.db.execute(purge_scout_table) as cur:
            for system in systems_to_scout:
                await cur.execute(insert_scout_system, (system.system, system.priority, system.rownum))
            if commit:
                await self.db.commit()

    async def rollback(self):
        await self.db.execute("ROLLBACK")

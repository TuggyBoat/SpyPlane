from typing import List

from spyplane.database.base_repository import BaseRepository
from spyplane.models.scout_system import ScoutSystem

insert_scout_system = '''
insert into scout_systems (system_name, priority, rownum) values (?,?,?);
'''
insert_post_system = '''
insert or ignore into scout_systems_posted (system_name, priority, rownum) values (?,?,?);
'''
update_post_system = '''
update scout_systems_posted set priority=?, rownum=? where system_name=?;
'''
select_scout_system = '''
select *
from scout_systems
where system_name=?;
'''

get_valid_systems_query = '''
select s.system_name, s.priority, s.rownum
from scout_systems s
join systems m on s.system_name = m.name
where s.priority != '' and printf("%d", s.priority) = s.priority
order by rownum
'''

remove_scouted_system = '''
delete from scout_systems_posted where system_name=?
'''

purge_scout = '''
delete from scout_systems
'''

purge_posted = '''
delete from scout_systems_posted
'''

get_post_systems = '''
select s.system_name, s.priority, s.rownum
from scout_systems_posted s
'''

get_invalid_systems_query = '''
select ss.system_name, ss.priority, ss.rownum
from scout_systems ss
left join (
%s
) m on ss.system_name = m.system_name
where m.system_name is null;
'''


class SystemsRepository(BaseRepository):

    async def get_invalid_systems(self) -> List[ScoutSystem]:
        return await self.get_systems(get_invalid_systems_query % get_valid_systems_query)

    async def get_valid_systems(self) -> List[ScoutSystem]:
        return await self.get_systems(get_valid_systems_query)

    async def get_carryover_systems(self) -> List[ScoutSystem]:
        return await self.get_systems(get_post_systems)

    async def get_system(self, system_name) -> ScoutSystem:
        async with self.db().execute(select_scout_system, [system_name]) as cur:
            row = await cur.fetchone()
        return ScoutSystem(row[0], row[1], row[2])

    async def purge_scout_systems(self) -> None:
        await self.db().execute(purge_scout)

    async def remove_scouted(self, system_name) -> None:
        await self.db().execute(remove_scouted_system, [system_name])
        print(f"Removed scout: {system_name}")

    async def get_systems(self, query) -> List[ScoutSystem]:
        async with self.db().execute(query) as cur:
            rows = await cur.fetchall()
        return [ScoutSystem(row[0], row[1], row[2]) for row in rows]

    async def write_system_to_post(self, systems_to_scout: List[ScoutSystem]):
        array_of_tuples = [(system.system, system.priority, system.rownum) for system in systems_to_scout]
        array_of_tuples_update = [(system.priority, system.rownum, system.system) for system in systems_to_scout]
        await self.db().executemany(insert_post_system, array_of_tuples)
        await self.db().executemany(update_post_system, array_of_tuples_update)

    async def write_system_to_scout(self, systems_to_scout: List[ScoutSystem]):
        await self.purge_scout_systems()
        array_of_tuples = [(system.system, system.priority, system.rownum) for system in systems_to_scout]
        await self.db().executemany(insert_scout_system, array_of_tuples)

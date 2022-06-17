import sqlite3
from typing import List

from ..sheets.scout_system import ScoutSystem

insert_scout_system = '''
insert into scout_systems (system_name, priority, rownum) values (?,?,?);
'''
select_scout_system = '''
select * 
from scout_systems 
where system_name = ?;
'''

get_valid_systems_query = '''
select s.system_name, s.priority, s.rownum 
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

    def __init__(self, path='./workspace/spyplane.db'):
        self.connection = sqlite3.connect(path)
        self.connection.set_trace_callback(print)
        self.exec = self.connection.execute

    def get_invalid_systems(self) -> List[ScoutSystem]:
        return self.get_systems(get_invalid_systems_query % get_valid_systems_query)

    def get_valid_systems(self) -> List[ScoutSystem]:
        return self.get_systems(get_valid_systems_query)

    def get_system(self, system_name) -> ScoutSystem:
        cur = self.connection.cursor()
        row = cur.execute(select_scout_system, [system_name]).fetchone()
        system = ScoutSystem(row[0], row[1], row[2])
        cur.close()
        return system

    def get_systems(self, query) -> List[ScoutSystem]:
        cur = self.connection.cursor()
        rows = cur.execute(query).fetchall()
        systems = [ScoutSystem(row[0], row[1], row[2]) for row in rows]
        cur.close()
        return systems

    def write_system_to_scout(self, systems_to_scout: List[ScoutSystem], commit=True):
        cur = self.connection.cursor()
        cur.execute(purge_scout_table)
        for system in systems_to_scout:
            cur.execute(insert_scout_system, (system.system, system.priority, system.rownum))
        if commit:
            self.connection.commit()
        cur.close()

    def begin_transaction(self):
        self.exec("BEGIN")

    def rollback_transaction(self):
        self.exec("ROLLBACK")

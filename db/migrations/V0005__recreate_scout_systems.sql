drop table scout_systems;
create table scout_systems
(
    "system_name" text primary key,
    "priority"    integer,
    "rownum"      integer
);

create table scout_systems_posted
(
    "system_name" text primary key,
    "priority"    integer,
    "rownum"      integer
);

insert into configuration (name, value, timestamp)
values ('carryover', 'true', 1655665882)

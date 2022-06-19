create table scout_history
(
    "id"          integer primary key autoincrement,
    "system_name" text not null,
    "username"    text not null,
    "userid"      integer not null,
    "timestamp"   integer not null
);


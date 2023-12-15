"""
Functions relating to databases used by spyplane.

Depends on: constants

Error handling: errors originating from Discord commands should be handled in their respective Cogs and outputted to user
                errors occuring on startup functions should be handled within those functions and outputted to terminal
"""

# libraries
import asyncio
import csv
import enum
import io
import sqlite3
import os
import tempfile
from io import BytesIO

import discord

# local classes
from ptn.spyplane.classes.ConfigData import ConfigData

# local constants
import ptn.spyplane.constants as constants
from ptn.spyplane.classes.TickData import TickData

"""
STARTUP FUNCTIONS
"""


# ensure all paths function for a clean install
def build_directory_tree_on_startup():
    print("Building directory tree...")
    try:
        os.makedirs(constants.DB_PATH, exist_ok=True)  # /database - the main database files
        os.makedirs(constants.SQL_PATH, exist_ok=True)  # /database/db_sql - DB SQL dumps
        os.makedirs(constants.BACKUP_DB_PATH, exist_ok=True)  # /database/backups - db backups
    except Exception as e:
        print(f"Error building directory tree: {e}")


build_directory_tree_on_startup()  # build directory structure


# build or modify database as needed on startup
async def build_database_on_startup():
    print("Building database...")
    try:
        database_table_map = {
            'config_data': {'obj': spyplane_db, 'create': config_table_create},
            'tick_times': {'obj': spyplane_db, 'create': tick_times_table_create},
            'scout_data': {'obj': spyplane_db, 'create': scout_data_table_create},
            'scout_system_data': {'obj': spyplane_db, 'create': scout_system_table_create}
        }

        for table_name in database_table_map:
            t = database_table_map[table_name]
            if not check_database_table_exists(table_name, t['obj']):
                create_missing_table(table_name, t['obj'], t['create'])
            else:
                print(f'{table_name} table exists, do nothing')
    except Exception as e:
        print(f"Error building database: {e}")

    interval = await get_scout_interval()
    print(f'Interval set to: {interval / 3600} hours')


# defining infraction table for database creation
config_table_create = '''
    CREATE TABLE config_data(
        config_setting TEXT NOT NULL UNIQUE,
        config_value TEXT NOT NULL
    )
    '''
tick_times_table_create = '''
    CREATE TABLE tick_times(
        entry_id INTEGER PRIMARY KEY,
        tick_time INTEGER NOT NULL
    )
'''
scout_data_table_create = '''
    CREATE TABLE scout_data(
        entry_id INTEGER PRIMARY KEY,
        system_name TEXT NOT NULL,
        username TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL
    )
'''
scout_system_table_create = '''
    CREATE TABLE scout_system_data(
        entry_id INTEGER PRIMARY KEY,
        system_name TEXT NOT NULL UNIQUE,
        last_update INTEGER NOT NULL,
        priority INTEGER NOT NULL
    )
'''


# function to check if a given table exists in a given database
def check_database_table_exists(table_name, database):
    """
    Checks whether a table exists in the database already.

    :param str table_name:  The database string name to create.
    :param sqlite.Connection.cursor database: The database to connect againt.
    :returns: A boolean state, True if it exists, else False
    :rtype: bool
    """
    print(f'Starting up - checking if {table_name} table exists or not')

    database.execute(f"SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{table_name}'")
    return bool(database.fetchone()[0])


# function to create a missing table / database
def create_missing_table(table, db_obj, create_stmt):
    """
    :param table:
    :param db_obj:
    :param create_stmt:
    """
    print(f'{table} table missing - creating it now')

    if os.path.exists(os.path.join(os.getcwd(), 'db_sql', f'{table}_dump.sql')):

        # recreate from backup file
        print('Recreating database from backup ...')
        with open(os.path.join(os.getcwd(), 'db_sql', f'{table}_dump.sql')) as f:

            sql_script = f.read()
            db_obj.executescript(sql_script)

    else:
        # Create a new version
        print('No backup found - Creating empty database')

        db_obj.execute(create_stmt)


"""
DATABASE OBJECT

Database connection, cursor, and lock
"""

# connect to infraction database
spyplane_conn = sqlite3.connect(constants.INFRACTIONS_DB_PATH)
spyplane_conn.row_factory = sqlite3.Row
spyplane_db = spyplane_conn.cursor()

# lock infraction db
spyplane_db_lock = asyncio.Lock()


async def insert_scout_log(system_name, username, user_id, timestamp):
    """
    Inserts a new scout_log into the database

    :param system_name:
    :param username:
    :param user_id:
    :param timestamp:
    :return: int
    """

    print(f'Inserting scout log for {username}.')

    try:
        await spyplane_db_lock.acquire()

        spyplane_db.execute(
            f"INSERT INTO scout_data (system_name, username, user_id, timestamp) VALUES (?, ?, ?, ?)",
            (system_name, username, user_id, timestamp)
        )
        spyplane_conn.commit()

        entry_id = spyplane_db.lastrowid

    finally:
        spyplane_db_lock.release()

    print(f"Scout log inserted with entry ID {entry_id}.")

    return entry_id


async def insert_tick(tick_time: int):
    """
    Inserts a tick into the database given a timestamp
    :param tick_time:
    :return: database entry id
    """
    try:
        await spyplane_db_lock.acquire()

        spyplane_db.execute(
            f"INSERT INTO tick_times (tick_time) VALUES ({tick_time})",
        )
        spyplane_conn.commit()

        entry_id = spyplane_db.lastrowid

    finally:
        spyplane_db_lock.release()

    print(f"Scout log inserted with entry ID {entry_id}.")

    return entry_id


async def get_last_tick():
    """
    Get the last inserted tick from database

    :return: list[TickData]
    """
    query = "SELECT * FROM tick_times ORDER BY entry_id DESC LIMIT 1"
    spyplane_db.execute(query)

    tick_data = [TickData(tick) for tick in spyplane_db.fetchall()]

    return tick_data


async def get_scout_interval():
    """
    :return: Returns the default interval or the set interval from the database
    """
    query = "SELECT * FROM config_data WHERE config_setting = 'scout_interval'"
    spyplane_db.execute(query)
    result = spyplane_db.fetchone()

    if result is None:
        try:
            await spyplane_db_lock.acquire()
            spyplane_db.execute(f"INSERT INTO config_data (config_setting, config_value) VALUES "
                                f"('scout_interval', {str(constants.default_scout_interval())})")
            spyplane_conn.commit()
            print('Inserted default scout interval into config db')
            return constants.default_scout_interval()

        finally:
            spyplane_db_lock.release()

    else:
        config = int(ConfigData(result).config_value)
        return config


async def get_all_configs():
    """
    Get every config from the database
    :return: list[ConfigData]
    """
    spyplane_db.execute("SELECT * FROM config_data")
    config_data = [ConfigData(config) for config in spyplane_db.fetchall()]
    return config_data


async def update_config(config_setting: str, config_value: str):
    """
    Updates the config given setting and value
    :param config_setting:
    :param config_value:
    """
    try:
        await spyplane_db_lock.acquire()

        update_sql = '''
            UPDATE config_data SET config_value = ? WHERE config_setting = ?
        '''

        spyplane_db.execute(update_sql, (config_value, config_setting))
        spyplane_conn.commit()
    finally:
        spyplane_db_lock.release()


async def update_system(system_name: str, last_update: int):
    """
    Updates the given system in the scout system database
    :param system_name: str
    :param last_update: int
    """
    try:
        await spyplane_db_lock.acquire()

        update_sql = '''UPDATE scout_system_data SET last_update = ? WHERE system_name = ?'''

        spyplane_db.execute(update_sql, (last_update, system_name))

    finally:
        spyplane_db_lock.release()


async def find_config(config_setting: str):
    """
    Get config from database
    :param config_setting:
    :return: returns result from query
    """
    query = f"SELECT * FROM config_data WHERE config_setting = '{config_setting}'"
    spyplane_db.execute(query)
    result = spyplane_db.fetchone()
    return ConfigData(result)


async def scouting_data_to_csv(interaction: discord.Interaction):
    spyplane_db.execute("SELECT * FROM scout_data")
    rows = spyplane_db.fetchall()

    # First, use StringIO to write CSV data as text
    with io.StringIO() as text_output:
        csv_writer = csv.writer(text_output)
        column_headers = [description[0] for description in spyplane_db.description]
        csv_writer.writerow(column_headers)
        csv_writer.writerows(rows)

        # Get the string from StringIO and encode it to bytes
        csv_data = text_output.getvalue().encode('utf-8')

    # Now, use BytesIO with the encoded data
    with io.BytesIO(csv_data) as binary_output:
        # Create a discord File object from the binary buffer
        discord_file = discord.File(fp=binary_output, filename='report.csv')

        # Send the file in the Discord message
        embed = discord.Embed(description='Here\'s the report', color=constants.EMBED_COLOUR_QU)
        await interaction.response.send_message(embed=embed, file=discord_file, ephemeral=True)


async def get_system_state_interval():
    """
    :return: Returns the default interval or the set interval from the database
    """
    query = "SELECT * FROM config_data WHERE config_setting = 'system_state_interval'"
    spyplane_db.execute(query)
    result = spyplane_db.fetchone()

    if result is None:
        try:
            await spyplane_db_lock.acquire()
            spyplane_db.execute(f"INSERT INTO config_data (config_setting, config_value) VALUES "
                                f"('system_state_interval', {str(constants.default_scout_interval())})")
            spyplane_conn.commit()
            print('Inserted default scout interval into config db')
            return constants.default_system_state_interval()

        finally:
            spyplane_db_lock.release()

    else:
        config = int(ConfigData(result).config_value)
        return config


async def get_monitoring_channel_id():
    """
    :return: Returns the default interval or the set interval from the database
    """
    query = "SELECT * FROM config_data WHERE config_setting = 'monitoring_channel_id'"
    spyplane_db.execute(query)
    result = spyplane_db.fetchone()

    if result is None:
        try:
            await spyplane_db_lock.acquire()
            spyplane_db.execute(f"INSERT INTO config_data (config_setting, config_value) VALUES "
                                f"('monitoring_channel_id', {str(constants.channel_monitoring())})")
            spyplane_conn.commit()
            print('Inserted default scout interval into config db')
            return constants.channel_monitoring()

        finally:
            spyplane_db_lock.release()

    else:
        config = int(ConfigData(result).config_value)
        return config


async def get_scout_emoji_id():
    """
        :return: Returns the default emoji id or the set emoji id from the database
        """
    query = "SELECT * FROM config_data WHERE config_setting = 'scout_emoji_id'"
    spyplane_db.execute(query)
    result = spyplane_db.fetchone()

    if result is None:
        try:
            await spyplane_db_lock.acquire()
            spyplane_db.execute(f"INSERT INTO config_data (config_setting, config_value) VALUES "
                                f"('scout_emoji_id', {str(constants.emoji_assassin())})")
            spyplane_conn.commit()
            print('Inserted default emoji id into config db')
            return constants.emoji_assassin()

        finally:
            spyplane_db_lock.release()

    else:
        config = int(ConfigData(result).config_value)
        return config

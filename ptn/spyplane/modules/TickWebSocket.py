import asyncio
import datetime

import socketio

from ptn.spyplane.constants import default_system_state_interval
from ptn.spyplane.database.database import get_last_tick, insert_tick
from ptn.spyplane.modules.Helpers import get_average_tick_times, clear_scout_messages
from ptn.spyplane.modules.SystemFactionStatesReporter import delayed_system_state_update, post_system_state_report, \
    force_state_update
from ptn.spyplane.modules.SystemScouter import delayed_scout_update, force_scout

# socket
sio = socketio.AsyncClient()
is_running = False


@sio.event
async def connect():
    print('Successful connection established with tick detector')


@sio.event
async def disconnect():
    print('Disconnected from tick detector')


# Tick message detection
@sio.event
async def message(data):
    print('Tick received:', data)
    await check_tick(data)


async def start_client():
    await sio.connect('https://tick.edcd.io/')
    await sio.wait()


def to_datetime(datetime_string: str):
    dt_object = datetime.datetime.fromisoformat(datetime_string)
    dt_obj_utc = dt_object.astimezone(datetime.timezone.utc)
    return dt_obj_utc.timestamp()


async def check_tick(data: str):
    print('Checking tick for change...')
    # convert tick to time.time() timestamp
    timestamp = int(to_datetime(data))

    # get last tick
    last_tick = await get_last_tick()

    try:
        last_tick = last_tick[0].tick_time
    except:
        last_tick = False
    print(last_tick < timestamp)
    # if this is the first tick
    if not last_tick:
        print('Populating tick table with first tick')
        await insert_tick(timestamp)
        await delayed_scout_update()
        await delayed_system_state_update()

    # if the tick is the same (happens when restarting/reconnecting)
    elif last_tick == timestamp:
        print('Ticks are equal, skipping...')
        # await backup_check(last_tick)
        return

    elif last_tick < timestamp and (timestamp - last_tick) > 43200:
        print(timestamp - last_tick)
        print('New tick detected')
        await insert_tick(timestamp)
        await delayed_scout_update()
        await delayed_system_state_update()
        # await backup_check(last_tick)

    if (timestamp - last_tick) < 43200:
        print('Tick was not more than 12 hours ahead of last, skipping...')


async def backup_check(last_tick):
    global is_running
    average_interval_seconds = int(get_average_tick_times() * 60 * 60)
    print('Checking for backup')
    if is_running:
        print('Backup is already running')
        return

    try:
        print('Backup is not running, running checking now')
        is_running = True
        while True:
            if last_tick:
                last_tick_time = datetime.datetime.fromtimestamp(last_tick)
                current_time = datetime.datetime.now()
                print((current_time - last_tick_time).total_seconds())
                if (current_time - last_tick_time).total_seconds() > 18000:
                    print('Forcing tick functions from backup')
                    await force_scout()
                    await post_system_state_report()
                    await force_state_update()
            await asyncio.sleep(18000 + average_interval_seconds)

    finally:
        is_running = False

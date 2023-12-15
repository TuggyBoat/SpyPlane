import asyncio
import time
from datetime import datetime

import discord

from ptn.spyplane.bot import bot
# import local constants
from ptn.spyplane.constants import channel_scout, emoji_assassin, role_scout, bot_guild
from ptn.spyplane.database.database import insert_scout_log, get_scout_interval, get_scout_emoji_id, get_last_tick
from ptn.spyplane.modules.ErrorHandler import CustomError
from ptn.spyplane.modules.Helpers import clear_scout_messages
from ptn.spyplane.modules.Sheets import update_row, get_systems, post_list_by_priority


async def post_scouting():
    """
    Posts all systems for scouting
    """
    # Get scouting channel
    guild = bot.get_guild(bot_guild())
    scout_channel = guild.get_channel(channel_scout())

    emoji = guild.get_emoji(await get_scout_emoji_id())
    if not emoji:
        emoji = guild.get_emoji(emoji_assassin())
    scout_role = guild.get_role(role_scout())

    # Get systems and priorities
    systems = await post_list_by_priority()

    # clear channel
    await clear_scout_messages()

    current_priority = '1'
    await scout_channel.send('## Primary List')
    for system in systems:
        # print(system[1]) - debug for system priorities
        # Check for transition in priority and send a message accordingly
        if system[1] != current_priority:
            if current_priority == '1':
                await scout_channel.send('## Secondary List')
            elif current_priority == '2':
                await scout_channel.send('## Tertiary List')
            current_priority = system[1]

        # Send the system message and add a reaction
        message = await scout_channel.send(system[0])
        await message.add_reaction(emoji)

    # Final message
    await scout_channel.send('System scouting updated ' + scout_role.mention)


async def delayed_scout_update():
    """
    Delay scouting for a set amount of time
    """
    # constants
    current_time = int(time.time())
    guild = bot.get_guild(bot_guild())
    scout_channel = guild.get_channel(channel_scout())
    scout_interval = await get_scout_interval()

    # get last tick
    last_tick = await get_last_tick()
    last_tick = last_tick[0].tick_time

    # if we are past the tick scout time
    time_at_scout = last_tick + scout_interval
    past_scout_time = time_at_scout <= current_time
    time_until_scout = time_at_scout - current_time
    print(f"Scout interval: {scout_interval}")

    # clear channel
    await clear_scout_messages()

    # if we are not past scout time
    if not past_scout_time:
        pending_message = await scout_channel.send(f'Spy Plane will take off <t:{time_at_scout}:R>')
        await asyncio.sleep(time_until_scout)  # sleep an amount of time
        await pending_message.delete()
    await post_scouting()
    print('Scouting post done.')


async def log_scout(system_name, member_name, member_id):
    """
    :param system_name:
    :param member_name:
    :param member_id:
    :return: int or False
    """
    print(f'Logging scout for {system_name} by {member_name}')
    try:
        # get timestamp format for sheets
        timestamp = time.time()
        dt_object = datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime('%d/%m/%Y %H:%M:%S')

        # update sheets
        await update_row(row_name=system_name, username=member_name, user_id=member_id, timestamp=formatted_time)

        # log to database
        return await insert_scout_log(system_name=system_name, username=member_name, user_id=member_id,
                                      timestamp=timestamp)

    except:
        print('Error in logging')
        return False

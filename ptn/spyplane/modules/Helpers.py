# imports
import asyncio
import pprint
import time
import urllib
from datetime import datetime, timedelta
from urllib.request import urlopen

import discord
import numpy
import requests
from discord import app_commands

from ptn.spyplane.bot import bot
from ptn.spyplane.constants import channel_scout, bot_guild
from ptn.spyplane.modules.ErrorHandler import CommandRoleError

# local constants

"""
Helpers for main functions
"""


async def clear_scout_messages():
    guild = bot.get_guild(bot_guild())
    scout_channel = guild.get_channel(channel_scout())

    # Clear messages
    messages = [message async for message in scout_channel.history(limit=None)]
    non_pinned_messages = [message for message in messages if not message.pinned]
    await scout_channel.delete_messages(non_pinned_messages)


"""
Check role helpers
"""


def get_role(ctx, id):  # takes a Discord role ID and returns the role object
    role = discord.utils.get(ctx.guild.roles, id=id)
    return role


async def checkroles_actual(interaction: discord.Interaction, permitted_role_ids):
    try:
        """
        Check if the user has at least one of the permitted roles to run a command
        """
        print(f"checkroles called.")
        author_roles = interaction.user.roles
        permitted_roles = [get_role(interaction, role) for role in permitted_role_ids]
        # print(author_roles)
        # print(permitted_roles)
        permission = True if any(x in permitted_roles for x in author_roles) else False
        # print(f'Permission: {permission}')
        return permission, permitted_roles
    except Exception as e:
        print(e)
    return permission


def check_roles(permitted_role_ids):
    async def checkroles(interaction: discord.Interaction):
        permission, permitted_roles = await checkroles_actual(interaction, permitted_role_ids)
        print("Inherited permission from checkroles")
        if not permission:  # raise our custom error to notify the user gracefully
            role_list = []
            for role in permitted_role_ids:
                role_list.append(f'<@&{role}> ')
                formatted_role_list = " • ".join(role_list)
            try:
                raise CommandRoleError(permitted_roles, formatted_role_list)
            except CommandRoleError as e:
                print(e)
                raise
        return permission

    return app_commands.check(checkroles)


"""
Average Tick Helper
"""


def get_past_7_days_ticks():
    """
    Gets past 7 days in ticks
    """
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    seven_days_ago_unix_timestamp = int(seven_days_ago.timestamp() * 1000)
    api_endpoint = "https://elitebgs.app/api/ebgs/v5/ticks"
    params = {"timeMin": seven_days_ago_unix_timestamp}
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        ticks = []
        for tick in data:
            ticks.append(tick["updated_at"])
        return ticks


def get_average_tick_times():
    """
    Gets the average interval between tick
    return: int
    """
    tick_times = get_past_7_days_ticks()
    # Convert to datetime objects
    tick_times = [datetime.fromisoformat(t.replace("Z", "+00:00")) for t in tick_times]

    # Calculate intervals (in hours or your preferred unit)
    intervals = [abs((tick_times[i] - tick_times[i + 1]).total_seconds() / 3600) for i in range(len(tick_times) - 1)]

    # Remove outliers using IQR
    Q1 = numpy.percentile(intervals, 25)
    Q3 = numpy.percentile(intervals, 75)
    IQR = Q3 - Q1

    # Define bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out outliers
    filtered_intervals = [i for i in intervals if lower_bound <= i <= upper_bound]

    # Calculate average interval
    average_interval = sum(filtered_intervals) / len(filtered_intervals)

    return average_interval

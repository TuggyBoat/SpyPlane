# imports
import asyncio
import pprint
import time
import urllib
from datetime import datetime
from urllib.request import urlopen

import discord
import requests
from discord import app_commands

from ptn.spyplane.bot import bot
from ptn.spyplane.constants import channel_scout, bot_guild
from ptn.spyplane.modules.ErrorHandler import CommandRoleError

# local constants

"""
Helpers for main functions
"""


def get_ebgs_systems(systems: list):
    """
    :param systems: list
    :return: dict
    """
    api_endpoint = "https://elitebgs.app/api/ebgs/v5/systems"

    # Construct the parameters dynamically
    params = {f'name[{index}]': system.strip() for index, system in enumerate(systems)}

    # GET request
    response = requests.get(api_endpoint, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        timestamps = {}

        for doc in data['docs']:
            system_name = doc['name']
            update_time = doc['updated_at']
            dt_obj = datetime.strptime(update_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp = dt_obj.timestamp()
            timestamps[system_name] = timestamp

        return timestamps
    else:
        # Handle errors or return False or an empty dictionary
        return False


def fetch_current_tick() -> int:
    hdr = {
        'User-Agent': 'curl/7.68.0',
        'Accept': '*/*'
    }
    link = "https://elitebgs.app/api/ebgs/v5/ticks"
    response = requests.get(link)
    return response.json()


print(fetch_current_tick())


def time_to_timestamp(date_str):
    date_format = "%d/%m/%Y %H:%M:%S"
    datetime_obj = datetime.strptime(date_str, date_format)

    return int(time.mktime(datetime_obj.timetuple()))


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

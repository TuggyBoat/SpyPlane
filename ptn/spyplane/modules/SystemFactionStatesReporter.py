import asyncio
import time
import traceback

import discord
import httpx

from ptn.spyplane import constants
from ptn.spyplane.bot import bot
from ptn.spyplane.constants import bot_guild
from ptn.spyplane.database.database import get_system_state_interval, get_monitoring_channel_id, get_last_tick
from ptn.spyplane.modules.Sheets import get_systems


async def get_faction_states_in_system(client: httpx.AsyncClient, systemName: str):
    api_endpoint = "https://elitebgs.app/api/ebgs/v5/systems"
    params = {'name': systemName.rstrip(), 'factionDetails': 'true'}

    expansion_factions = set()
    retreat_factions = set()
    # This dict will now be keyed by systemName.
    other_states_system_info = {}

    try:
        response = await client.get(api_endpoint, params=params, timeout=10.0)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors

        data = response.json()
        data = data['docs'][0]
        if not data.get('factions'):
            print(f"No factions found for {systemName}")
            return retreat_factions, expansion_factions, other_states_system_info

        for faction in data['factions']:
            faction_details = faction.get('faction_details')
            faction_presence = faction_details.get('faction_presence')
            active_states = faction_presence.get('active_states', [])
            pending_states = faction_presence.get('pending_states', [])
            all_states = active_states + pending_states

            faction_name = faction.get('name', 'Unknown Faction')

            if any(state['state'] == 'expansion' for state in all_states):
                expansion_factions.add(faction_name)
            if any(state['state'] == 'retreat' for state in all_states):
                retreat_factions.add(faction_name)

            # Collect other states (excluding Expansion and Retreat)
            other_states = [state for state in all_states if state['state'] not in ('expansion', 'retreat')]
            if other_states:
                # Group by system. Create a sub-dictionary for the system if it doesn't exist.
                if systemName not in other_states_system_info:
                    other_states_system_info[systemName] = {}
                other_states_system_info[systemName][faction_name] = {
                    'active_states': active_states,
                    'pending_states': pending_states
                }

    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code} for {systemName}: {e}")
    except httpx.RequestError as e:
        print(f"Request error for {systemName}: {e}")
    except Exception as e:
        print(f"Unexpected error fetching data for {systemName}: {e}")
        traceback.print_exc()

    return retreat_factions, expansion_factions, other_states_system_info


async def get_faction_states_in_scout_systems(scoutList: list):
    """
    Gets a system's factions and their states, splitting expansion and retreat factions.
    :param scoutList: list of system names
    :return: set (retreating factions), set (expansion factions), dict (other states grouped by system)
    """
    all_expansion_factions = set()
    all_retreating_factions = set()
    all_other_states_systems_info = {}

    print('Call for system states, gathering...')

    async with httpx.AsyncClient() as client:
        tasks = [
            get_faction_states_in_system(client, system[0] if isinstance(system, list) else system)
            for system in scoutList
        ]
        results = await asyncio.gather(*tasks)

    for retreat_factions, expansion_factions, other_states_system_info in results:
        all_expansion_factions.update(expansion_factions)
        all_retreating_factions.update(retreat_factions)
        # Merge the per-system data into the master dictionary.
        for system, factions in other_states_system_info.items():
            if system not in all_other_states_systems_info:
                all_other_states_systems_info[system] = factions
            else:
                all_other_states_systems_info[system].update(factions)

    print('Gathered systems states, returning...')
    return all_retreating_factions, all_expansion_factions, all_other_states_systems_info


async def create_faction_states_embed(systemList):
    retreating_factions, expanding_factions, other_states_factions = await get_faction_states_in_scout_systems(systemList)
    body = '**Expanding Factions**'
    for expanding_faction in expanding_factions:
        body += '\n' + expanding_faction

    body += "\n\n**Retreating Factions**"
    for retreating_faction in retreating_factions:
        body += '\n' + retreating_faction

    body += '\n\n**Other States in Systems**'
    # Now, each key is a system name.
    for system, factions in other_states_factions.items():
        body += f'\n**{system}**:'
        for faction_name, state_info in factions.items():
            active_states = ', '.join([state['state'] for state in state_info.get('active_states', [])])
            pending_states = ', '.join([state['state'] for state in state_info.get('pending_states', [])])
            body += f'\n- {faction_name}'
            if active_states:
                body += f' - Active: {active_states}'
            if pending_states:
                body += f' - Pending: {pending_states}'

    print('Generated embed for faction states')
    embed = discord.Embed(title='Faction States in PTN Space', description=body, color=constants.EMBED_COLOR_AGENT)
    return embed


async def post_system_state_report():
    guild = bot.get_guild(bot_guild())
    monitoring_channel = guild.get_channel(await get_monitoring_channel_id())
    embed = await create_faction_states_embed(get_systems())
    await monitoring_channel.send(embed=embed)


async def delayed_system_state_update():
    """
    Runs the system states report after a set amount of time
    """
    system_state_interval = await get_system_state_interval()
    current_time = int(time.time())

    # get last tick
    last_tick = await get_last_tick()
    last_tick = last_tick[0].tick_time

    # if we are past the states time
    time_at_states = last_tick + system_state_interval
    past_states_time = time_at_states <= current_time
    time_until_states = time_at_states - current_time

    print('System State Reporting interval is ' + str(system_state_interval))
    if not past_states_time:
        await asyncio.sleep(time_until_states)  # sleep an amount of time
    await post_system_state_report()


async def force_state_update():
    system_state_interval = await get_system_state_interval()
    current_time = int(time.time())
    expected_tick = current_time - 18000
    time_at_states = expected_tick + system_state_interval
    past_states_time = time_at_states <= current_time
    time_until_states = time_at_states - current_time
    print('System State Reporting interval is ' + str(system_state_interval))
    if not past_states_time:
        await asyncio.sleep(time_until_states)  # sleep an amount of time
    await post_system_state_report()

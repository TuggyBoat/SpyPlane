import asyncio
from asyncio.subprocess import PIPE, STDOUT
from discord import Interaction, app_commands
import discord

from spyplane._metadata import __version__
from spyplane.constants import log
from spyplane.services.config_service import ConfigService
from spyplane.services.daily_faction_state_service import DailyFactionStateService
from spyplane.services.sync_service import SyncService
from spyplane.services.systems_posting_service import SystemsPostingService
from spyplane.spy_plane import bot


class Commands:
    def __init__(self):
        pass


@bot.tree.command()
async def spy_plane_ping(interaction: Interaction):
    """Check if assets are blown"""
    await interaction.response.send_message(
        f'**Agent {bot.user.name} reporting in. Ready for clandestine operations**')


@bot.tree.command()
async def spy_plane_version(interaction: Interaction):
    """Agent experience level"""
    print(f'User {interaction.user.name} requested the version: {__version__}.')
    await interaction.response.send_message(
        f"Bagman is on station and awaiting orders. {bot.user.name} is on version: {__version__}."
    )


@bot.tree.command(name='spy_plane_launch')
async def post_systems(interaction: Interaction):
    """Begin HUMINT and Infiltration operations: Posts the systems to scout in pre-assigned dead drops"""
    await interaction.response.defer(ephemeral=True)
    print(f'User {interaction.user.name} is posting the systems to scout: {__version__}.')
    await SystemsPostingService().publish_systems_to_scout()
    await interaction.followup.send(f"Spy plane is now on the prowl!")


@bot.tree.command(name='spy_plane_report')
async def report(interaction: Interaction):
    """Classifeid HUMINT report on systems monitored"""
    await interaction.response.defer()
    print(f'User {interaction.user.name} is requesting report of monitored systems: {__version__}.')
    await DailyFactionStateService().notify_daily_news(interaction.channel)
    await interaction.followup.send(f"Classified surveillance Report | Faction Operative eyes-only")


@bot.tree.command()
async def spy_plane_sync(interaction: Interaction):
    """Transfer orders from command to field agents. Codeword: SyncSheet2DB"""
    print(f'User {interaction.user.name} is syncing the DB with sheet on systems to scout: {__version__}.')
    await interaction.response.defer()
    await SyncService().sync_db_sheet()
    await interaction.followup.send(f"Spy plane is fueled and ready to go")


@bot.tree.command()
async def spy_plane_config_dump(interaction: Interaction):
    """Playback of standard operating protocols"""
    print(f'User {interaction.user.name} is dumping config: {__version__}.')
    embed = await ConfigService().dump_config_embed()
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='spy_plane_config')
@app_commands.describe(
    name='Name of the config: Can be `interval_hours` or `carryover` ',
    value='Value: For `interval_hours` should be a number 1 to 24. For `carryover` it should be `true` or `false`',
)
async def config(interaction: Interaction, name: str, value: str):
    """Assign standard operating protocols"""
    print(f'User {interaction.user.name} is attempting to set config {name} to {value}: {__version__}.')
    message = await ConfigService().update_config(name, value)
    print(message)
    await interaction.response.send_message(message)


@bot.tree.command(name='spy_plane_emoji')
@app_commands.describe(
    id='Emoji ID'
)
async def emoji_test_utility(interaction: Interaction, id: str):
    """There is no hidden data encoded in emojis. None at all. Even Spies need to express emotions"""
    emoji = bot.get_emoji(int(id))
    message = await interaction.channel.send(f'Emoji for ID: {emoji}')
    await message.add_reaction(bot.emoji_bullseye)
    log(' '.join([f'{e.name}-{e.id}' for e in bot.emojis]))
    await interaction.response.send_message(f"Emoji cipher test completed")


@bot.tree.command()
async def spy_plane_operations_report(interaction: Interaction):
    """Top Secret: Classified agent activity report. Faction Command Eyes-Only."""
    await interaction.response.defer()
    await interaction.channel.send("Our top analyst is on it..")
    exitcode = await run_export_script(interaction.channel.send)
    if exitcode==0:
        print("[INFO] Export completed successfully.")
        await interaction.channel.send(file=discord.File("./workspace/faction_command_eyesonly.csv"))
        await interaction.followup.send(f"[Top Secret] Agent Activity Report. Eyes-Only Faction Command")
    else:
        print(f"[INFO] Export failed with exitcode: {exitcode}")
        await interaction.followup.send("Asset compromised. Report failed. Escalate to flight command")


async def run_export_script(send=None):
    cmd = './export_scout_history.sh'
    print("[INFO] Starting Export...")
    process = await asyncio.create_subprocess_shell(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    await process.wait()
    return process.returncode
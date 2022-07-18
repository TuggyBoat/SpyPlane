from discord import Interaction, app_commands

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


@bot.tree.command(name='spy_plane_ping', description='Ping the bot')
async def spy_plane_ping(interaction: Interaction):
    """Ping"""
    await interaction.response.send_message(
        f'**Agent {bot.user.name} reporting in. Ready for clandestine operations**')


@bot.tree.command(name='spy_plane_version', description="Logs the bot version")
async def version(interaction: Interaction):
    """Logs the version"""
    print(f'User {interaction.user.name} requested the version: {__version__}.')
    await interaction.response.send_message(
        f"Bagman is on station and awaiting orders. {bot.user.name} is on version: {__version__}."
    )


@bot.tree.command(name='spy_plane_launch', description="Posts the systems to scout")
async def post_systems(interaction: Interaction):
    """Post systems to scout"""
    await interaction.response.defer(ephemeral=True)
    print(f'User {interaction.user.name} is posting the systems to scout: {__version__}.')
    await SystemsPostingService().publish_systems_to_scout()
    await interaction.followup.send(f"Spy plane is now on the prowl!")

@bot.tree.command(name='spy_plane_report', description="Show the current status of monitored systems")
async def report(interaction: Interaction):
    """Show the current status of monitored systems"""
    await interaction.response.defer(ephemeral=True)
    print(f'User {interaction.user.name} is requesting report of monitored systems: {__version__}.')
    await DailyFactionStateService().notify_daily_news(interaction.channel)
    await interaction.followup.send(f"Spy plane report complete.")


@bot.tree.command(name='spy_plane_sync', description="syncs the db to sheets")
async def sync_systems(interaction: Interaction):
    """Sync systems sheet and db"""
    print(f'User {interaction.user.name} is syncing the DB with sheet on systems to scout: {__version__}.')
    await interaction.response.defer()
    await SyncService().sync_db_sheet()
    await interaction.followup.send(f"Spy plane is fueled and ready to go")


@bot.tree.command(name='spy_plane_config_dump', description="shows the current bot config")
async def dump_config(interaction: Interaction):
    """Dumps the bot configuration"""
    print(f'User {interaction.user.name} is dumping config: {__version__}.')
    embed = await ConfigService().dump_config_embed()
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='spy_plane_config', description="configures the bot behavior")
@app_commands.describe(
    name='Name of the config: Can be `interval_hours` or `carryover` ',
    value='Value: For `interval_hours` should be a number 1 to 24. For `carryover` it should be `true` or `false`',
)
async def config(interaction: Interaction, name: str, value: str):
    """Configures the bot behavior"""
    print(f'User {interaction.user.name} is attempting to set config {name} to {value}: {__version__}.')
    message = await ConfigService().update_config(name, value)
    print(message)
    await interaction.response.send_message(message)


@bot.tree.command(name='spy_plane_emoji', description="Utility to test the emoji availability in a server")
@app_commands.describe(
    id='Emoji ID'
)
async def emoji_test_utility(interaction: Interaction, id: str):
    """Post systems to scout"""
    emoji = bot.get_emoji(int(id))
    message = await interaction.channel.send(f'Emoji for ID: {emoji}')
    await message.add_reaction(bot.emoji_bullseye)
    log(' '.join([f'{e.name}-{e.id}' for e in bot.emojis]))
    await interaction.response.send_message(f"Emoji support test completed")

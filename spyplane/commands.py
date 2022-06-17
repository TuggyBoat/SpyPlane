from spyplane._metadata import __version__
from spyplane.database.systems_repository import SystemsRepository
from spyplane.messaging.systems_posting import SystemsPosting
from spyplane.services.sync_service import SyncService
from spyplane.spy_plane import bot
from discord import Interaction, app_commands


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
    await interaction.response.defer()
    print(f'User {interaction.user.name} is posting the systems to scout: {__version__}.')
    valid_systems = SystemsRepository().get_valid_systems()
    posting = SystemsPosting(interaction.channel)
    await posting.publish_systems_to_scout(valid_systems)
    await interaction.followup.send(f"Spy plane is now on the prowl!")

@bot.tree.command(name='spy_plane_sync', description="syncs the db to sheets")
async def sync_systems(interaction: Interaction):
    """Post systems to scout"""
    print(f'User {interaction.user.name} is syncing the DB with sheet on systems to scout: {__version__}.')
    await interaction.response.defer()
    # sqlite3 operations needs to run in same thread that it was created on
    SyncService().sync_db_sheet()
    await interaction.followup.send(f"Spy plane is fueled and ready to go")

@bot.tree.command(name='spy_plane_emoji', description="Utility to test the emoji availability in a server")
@app_commands.describe(
    id='Emoji ID'
)
async def emoji_test_utility(interaction: Interaction, id: str):
    """Post systems to scout"""
    emoji = bot.get_emoji(int(id))
    message = await interaction.channel.send(f'Emoji for ID: {emoji}')
    await message.add_reaction('✅' if emoji is None else emoji)
    await interaction.response.send_message(f"Emoji support: {' '.join([f'{e.name}-{e.id}' for e in bot.emojis])}")


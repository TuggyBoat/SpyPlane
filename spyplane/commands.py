from spyplane._metadata import __version__
from spyplane.tick_detection import TickDetection
from spyplane.spy_plane import bot
from discord import Interaction


class Commands:
    def __init__(self):
        self.tick = TickDetection()

    @bot.tree.command(name='spy_plane_ping', description='Ping the bot')
    async def spy_plane_ping(self, interaction: Interaction):
        """SpyPlane: Ping"""
        await interaction.response.send_message(
            f'**Agent {bot.user.name} reporting in. Ready for clandestine operations**')

    @bot.tree.command(name='spy_plane_version', description="Logs the bot version")
    async def version(self, interaction: Interaction):
        """SpyPlane: Logs the version"""
        print(f'User {interaction.user.author} requested the version: {__version__}.')
        await interaction.response.send_message(
            f"Bagman is on station and awaiting orders. {bot.user.name} is on version: {__version__}."
        )

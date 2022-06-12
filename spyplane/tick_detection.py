import discord
from discord.ext import commands

from spyplane.constants import BGS_BOT_USER_ID


class TickDetection(commands.Cog):

    def __init__(self):
        """
        We want to read from the tick detection channel the last tick message.
        """
        pass

    def validate_message(self, message: discord.message.Message):
        # This gets called from on_message directly, so we know we are in the right channel, we need to now check
        # whether the message is a 'tick' message or not

        # Ensure this is from the bot user account
        if message.author.id != BGS_BOT_USER_ID:
            return

        # Ok it is from the BGSBot, check if it is a tick message
        if 'Tick Detected' not in message and 'Latest Tick At' not in message:
            return

        print('Tick detection message found!')

        # Now we detected a tick, we need to do something with the event/notification

import discord
from discord import RawReactionActionEvent
from discord.ext import commands
import asyncio
import socketio

from ptn.spyplane.bot import bot
from ptn.spyplane.constants import channel_scout, emoji_assassin, channel_botspam
from ptn.spyplane.modules.ErrorHandler import CustomError
from ptn.spyplane.modules.SystemScouter import log_scout
import ptn.spyplane.constants as constants


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        # get the message and details
        channel = bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        guild = bot.get_guild(payload.guild_id)
        spam_channel = guild.get_channel(channel_botspam())

        scout_channel = payload.channel_id == channel_scout()
        if not scout_channel:
            # print(f'Wrong channel {payload.channel_id} vs {channel_scout()}')
            return

        if payload.user_id == bot.user.id:
            # print('Bot user')
            return

        if payload.emoji.id != emoji_assassin():
            # print('Wrong emoji')
            return

        if message.pinned:
            print('Pinned message')
            return

        print(f'Scout called for {message.content}')

        system = message.content
        scouter = payload.member
        scouter_id = scouter.id

        await message.delete()

        logged_scout = await log_scout(system_name=system, member_name=scouter.name, member_id=scouter_id)

        if not logged_scout:
            error_embed = discord.Embed(color=constants.EMBED_COLOUR_ERROR, description='Could not log scout!\n'
                                                                                        f'`System: {system}` | Scouter: {scouter.mention}')
            spam_channel.send(embed=error_embed)


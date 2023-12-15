# discord.py
import discord
from discord import app_commands
from discord.ext import commands

# import bot
from ptn.spyplane.bot import bot

# local constants
from ptn.spyplane._metadata import __version__
import ptn.spyplane.constants as constants
from ptn.spyplane.constants import role_council, role_mod
# local modules
from ptn.spyplane.modules.ErrorHandler import on_app_command_error

"""
A primitive global error handler for text commands.

returns: error message to user and log
"""


class ModCommands(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

        # ping command to check if the bot is responding

    @commands.command(name='ping', aliases=['hello', 'ehlo', 'helo'],
                      help='Use to check if spyplane is online and responding.')
    @commands.has_any_role(*constants.any_elevated_role)
    async def ping(self, ctx):
        print(f"{ctx.author} used PING in {ctx.channel.name}")
        embed = discord.Embed(
            title="🟢 MOD BOT ONLINE",
            description=f"🔨<@{bot.user.id}> connected, version **{__version__}**.",
            color=constants.EMBED_COLOUR_OK
        )
        await ctx.send(embed=embed)

        # command to sync interactions - must be done whenever the bot has appcommands added/removed

    @commands.command(name='sync', help='Synchronise spyplane interactions with server')
    @commands.has_any_role(*constants.any_elevated_role)
    async def sync(self, ctx):
        print(f"Interaction sync called from {ctx.author.display_name}")
        async with ctx.typing():
            try:
                bot.tree.copy_global_to(guild=constants.guild_obj)
                await bot.tree.sync(guild=constants.guild_obj)
                print("Synchronised bot tree.")
                await ctx.send("Synchronised bot tree.")
            except Exception as e:
                print(f"Tree sync failed: {e}.")
                return await ctx.send(f"Failed to sync bot tree: {e}")
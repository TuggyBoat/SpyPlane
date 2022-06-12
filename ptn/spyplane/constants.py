import ast
import os

from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv, find_dotenv

# Get the discord token from the local .env file. Deliberately not hosted in the repo or Discord takes the bot down
# because the keys are exposed. DO NOT HOST IN THE REPO. Seriously do not do it ...
load_dotenv(find_dotenv())

# Common values

BGS_BOT_USER_ID = 332846508888031232

# Production values
PROD_DISCORD_GUILD = 800080948716503040  # PTN Discord server
PROD_DB_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'spyplane.db')
PROD_DB_DUMPS_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'dumps', 'spyplane.sql')
PROD_TICK_DETECTION_CHANNEL_ID = 829215577527812096

# TODO: Update this out of #spy-plane
PROD_SPY_PLANE_CHANNEL_ID = 873124212406099988

# Test server values
TEST_DISCORD_GUILD = 818174236480897055  # test Discord server
TEST_DB_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'spyplane.db')
TEST_DB_DUMPS_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'dumps', 'spyplane.sql')

TEST_SPY_PLANE_CHANNEL_ID = 878369147640234065
TEST_TICK_DETECTION_CHANNEL_ID = 879041976668946532

_production = ast.literal_eval(os.environ.get('PTN_SPY_PLANE', 'False'))

# Check the folder exists
if not os.path.exists(os.path.dirname(PROD_DB_PATH)):
    print(f'Folder {os.path.dirname(PROD_DB_PATH)} does not exist, making it now.')
    os.mkdir(os.path.dirname(PROD_DB_PATH))

# check the dumps folder exists
if not os.path.exists(os.path.dirname(PROD_DB_DUMPS_PATH)):
    print(f'Folder {os.path.dirname(PROD_DB_DUMPS_PATH)} does not exist, making it now.')
    os.mkdir(os.path.dirname(PROD_DB_DUMPS_PATH))


TOKEN = os.getenv('SPYPLANE_DISCORD_TOKEN_PROD') if _production else os.getenv('SPYPLANE_DISCORD_TOKEN_TESTING')

# The bot object:
bot = commands.Bot(command_prefix='s.', intents=Intents.all())
slash = SlashCommand(bot, sync_commands=True)


def bot_guild_id():
    """
    Returns the bots guild ID

    :returns: The guild ID value
    :rtype: int
    """
    return PROD_DISCORD_GUILD if _production else TEST_DISCORD_GUILD


def get_bot_control_channel():
    """
    Returns the channel ID for the bot control channel.

    :return: The channel ID
    :rtype: int
    """
    return PROD_SPY_PLANE_CHANNEL_ID if _production else TEST_SPY_PLANE_CHANNEL_ID


def get_tick_detection_channel():
    """
    Gets the channel we monitor for the tick detection logics.

    :return: The channel ID
    :rtype: int
    """
    return PROD_TICK_DETECTION_CHANNEL_ID if _production else TEST_TICK_DETECTION_CHANNEL_ID
"""
Constants used throughout SPYPLANE.

Depends on: nothing
"""

# libraries
import ast
import os
import discord
import gspread
from discord.ext import commands
from dotenv import load_dotenv

# Define whether the bot is in testing or live mode. Default is testing mode.
_production = ast.literal_eval(os.environ.get('PTN_SPYPLANE_SERVICE', 'False'))

# define paths
TESTING_DATA_PATH = os.path.join(os.getcwd(), 'data')  # defines the path for use in a local testing environment
DATA_DIR = os.getenv('PTN_SPYPLANE_DATA_DIR', TESTING_DATA_PATH)

# database paths
DB_PATH = os.path.join(DATA_DIR, 'database')  # path to database directory
INFRACTIONS_DB_PATH = os.path.join(DATA_DIR, 'database', 'spyplane.db')  # path to infractions database
BACKUP_DB_PATH = os.path.join(DATA_DIR, 'database', 'backups')  # path to use for direct DB backups
SQL_PATH = os.path.join(DATA_DIR, 'database', 'db_sql')  # path to use for SQL dumps

# Get the discord token from the local .env file. Deliberately not hosted in the repo or Discord takes the bot down
# because the keys are exposed. DO NOT HOST IN THE PUBLIC REPO.
# load_dotenv(os.path.join(DATA_DIR, '.env'))
load_dotenv(os.path.join(DATA_DIR, '.env'))

# google credentials
gc = gspread.service_account(filename=os.path.join(DATA_DIR, 'spyplane-394209-39d59161dedb.json'))

# define bot token
TOKEN = os.getenv('SPYPLANE_DISCORD_TOKEN_PROD') if _production else os.getenv('SPYPLANE_DISCORD_TOKEN_TESTING')

# ebgs
PTN_FACTION_ID = '612402938c6309f8d8558331'

# Production variables
PROD_DISCORD_GUILD = 800080948716503040  # PTN server ID
PROD_CHANNEL_BOTSPAM = 801258393205604372  # PTN bot-spam channel
PROD_CHANNEL_SCOUT = 878536094503829524
PROD_CHANNEL_MONITORING = 829215577527812096
PROD_ROLE_COUNCIL = 800091021852803072  # PTN Council role
PROD_ROLE_MOD = 813814494563401780  # PTN Mod role
PROD_ROLE_OP = 948206870491959317  # PTN Operator Role
PROD_ROLE_SCOUT = 938507320214839306  # PTN Scout Role
PROD_ROLE_SUPPORTER = 879491967157944381  # PTN Faction Supporter Role
PROD_EMOJI_TARGET = 806498760586035200  # PTN Assassin Emoji
PROD_DEFAULT_SCOUT_INTERVAL = 14400  # PTN Post Delay in seconds
PROD_DEFAULT_STATES_INTERVAL = 43200  # PTN EBGS Faction States Delay in seconds

# TUG Testing variables
TEST_DISCORD_GUILD = 682302487658496057  # PANTS server ID
TEST_CHANNEL_BOTSPAM = 1182782400141467718  # PANTS bot spam channel
TEST_CHANNEL_SCOUT = 1182773459273666720
TEST_CHANNEL_MONITORING = 1183527106039267438
TEST_ROLE_COUNCIL = 1166198689388314714  # PANTS Council role
TEST_ROLE_MOD = 1166198849975627866  # PANTS Mod role
TEST_ROLE_OP = 1166199159028723793  # PANTS Operator Role
TEST_ROLE_SUPPORTER = 1182909095322341397
TEST_ROLE_SCOUT = 1182909858148790333
TEST_EMOJI_TARGET = 1006810326953635891
TEST_DEFAULT_SCOUT_INTERVAL = 30  # PTN Post Delay in seconds
TEST_DEFAULT_STATES_INTERVAL = 60  # PTN EBGS Faction States Delay in seconds

# PANTS Variables
# TEST_DISCORD_GUILD = 818174236480897055  # PANTS server ID
# TEST_CHANNEL_BOTSPAM = 1183552513874591845  # PANTS bot spam channel
# TEST_CHANNEL_SCOUT = 878369147640234065
# TEST_CHANNEL_MONITORING = 1183552554798424145
# TEST_ROLE_COUNCIL = 877586918228000819  # PANTS Council role
# TEST_ROLE_MOD = 903292469049974845  # PANTS Mod role
# TEST_ROLE_OP = 1155985589200502844  # PANTS Operator Role
# TEST_ROLE_SUPPORTER = 1182909095322341397
# TEST_ROLE_SCOUT = 987800734819024977
# TEST_EMOJI_TARGET = 848957573792137247
# TEST_DEFAULT_SCOUT_INTERVAL = 30  # PTN Post Delay in seconds
# TEST_DEFAULT_STATES_INTERVAL = 60  # PTN EBGS Faction States Delay in seconds


# Embed colours
EMBED_COLOUR_ERROR = 0x800000  # dark red
EMBED_COLOUR_QU = 0x00d9ff  # que?
EMBED_COLOUR_OK = 0x80ff80  # we're good here thanks, how are you?
EMBED_COLOR_AGENT = 0xeb6a5c # redish

# random gifs and images
error_gifs = [
    'https://media.tenor.com/-DSYvCR3HnYAAAAC/beaker-fire.gif',  # muppets
    'https://media.tenor.com/M1rOzWS3NsQAAAAC/nothingtosee-disperse.gif',  # naked gun
    'https://media.tenor.com/oSASxe-6GesAAAAC/spongebob-patrick.gif',  # spongebob
    'https://media.tenor.com/u-1jz7ttHhEAAAAC/angry-panda-rage.gif'  # panda smash
]


# images and icons used in embeds


# define constants based on prod or test environment
def bot_guild():
    return PROD_DISCORD_GUILD if _production else TEST_DISCORD_GUILD


guild_obj = discord.Object(bot_guild())


def channel_botspam():
    return PROD_CHANNEL_BOTSPAM if _production else TEST_CHANNEL_BOTSPAM


def channel_scout():
    return PROD_CHANNEL_SCOUT if _production else TEST_CHANNEL_SCOUT

def channel_monitoring():
    return PROD_CHANNEL_MONITORING if _production else TEST_CHANNEL_MONITORING

def role_council():
    return PROD_ROLE_COUNCIL if _production else TEST_ROLE_COUNCIL


def role_mod():
    return PROD_ROLE_MOD if _production else TEST_ROLE_MOD


def role_supporter():
    return PROD_ROLE_SUPPORTER if _production else TEST_ROLE_SUPPORTER


def role_scout():
    return PROD_ROLE_SCOUT if _production else TEST_ROLE_SCOUT

def role_operative():
    return PROD_ROLE_OP if _production else TEST_ROLE_OP


def emoji_assassin():
    return PROD_EMOJI_TARGET if _production else TEST_EMOJI_TARGET

def default_scout_interval():
    return PROD_DEFAULT_SCOUT_INTERVAL if _production else TEST_DEFAULT_SCOUT_INTERVAL

def default_system_state_interval():
    return PROD_DEFAULT_STATES_INTERVAL if _production else TEST_DEFAULT_STATES_INTERVAL


any_elevated_role = [role_council(), role_mod()]
op_plus = [*any_elevated_role, role_operative()]

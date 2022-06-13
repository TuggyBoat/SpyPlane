import ast
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

flag_production = ast.literal_eval(os.environ.get('PRODUCTION', 'False'))

# Common environment variables
GDRIVE_TOKEN = os.path.join(os.getcwd(), 'token.json') if "/tests" not in os.getcwd() else os.path.join(os.getcwd(), '../token.json') # CWD = /tests/ for tests
BGS_BOT_USER_ID = os.getenv('BGS_BOT_USER_ID')
DB_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'spyplane.db')
DB_DUMPS_PATH = os.path.join(os.path.expanduser('~'), 'spyplane', 'dumps', 'spyplane.sql')

# Environment specific vars
EMOJI_BULLSEYE = 984187689781833748 if flag_production else 985030917246554152
TOKEN = os.getenv('SPYPLANE_DISCORD_TOKEN_PROD') if flag_production else os.getenv('SPYPLANE_DISCORD_TOKEN_TESTING')
APPLICATION_ID = os.getenv('APPLICATION_ID_PROD') if flag_production else os.getenv('APPLICATION_ID_TESTING')
GUILD_ID = os.getenv('PROD_DISCORD_GUILD') if flag_production else os.getenv('TEST_DISCORD_GUILD')
CONTROL_CHANNEL = int(os.getenv('PROD_SPY_PLANE_CHANNEL_ID')) if flag_production else \
    int(os.getenv('TEST_SPY_PLANE_CHANNEL_ID'))
TICK_CHANNEL = int(os.getenv('PROD_TICK_DETECTION_CHANNEL_ID')) if flag_production else \
    int(os.getenv('TEST_TICK_DETECTION_CHANNEL_ID'))

# Check the folder exists
if not os.path.exists(os.path.dirname(DB_PATH)):
    print(f'Folder {os.path.dirname(DB_PATH)} does not exist, making it now.')
    os.mkdir(os.path.dirname(DB_PATH))

# check the dumps folder exists
if not os.path.exists(os.path.dirname(DB_DUMPS_PATH)):
    print(f'Folder {os.path.dirname(DB_DUMPS_PATH)} does not exist, making it now.')
    os.mkdir(os.path.dirname(DB_DUMPS_PATH))

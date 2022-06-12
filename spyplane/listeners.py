from spyplane._metadata import __version__
from spyplane.tick_detection import TickDetection
from spyplane.constants import CONTROL_CHANNEL, TICK_CHANNEL, BGS_BOT_USER_ID
from spyplane.spy_plane import bot


class Listeners:
    """
    Importing this module helps to ensure the annotated methods in this module are registered
    This class prevents the imports optimizer from removing this module
    """
    def __init__(self):
        pass


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord server. Version: {__version__}')
    bot_channel = bot.get_channel(CONTROL_CHANNEL)
    await bot_channel.send(f'{bot.user.name} has connected to Discord server. Version: {__version__}')


@bot.event
async def on_disconnect():
    print(f'Spy Plane has disconnected from discord server. Version: {__version__}.')


@bot.event
async def on_error(event, *args, **kwargs):
    print(event)
    print(args)
    print(kwargs)


@bot.event
async def on_message(msg):
    if msg.author.id == bot.user.id:
        # Skip through, do not try to process the bots own messages or we will loop forever.
        pass
    elif msg.author.id == BGS_BOT_USER_ID and msg.channel.id == TICK_CHANNEL:
        # Route this to the tick detection handler
        TickDetection().validate_message(msg)

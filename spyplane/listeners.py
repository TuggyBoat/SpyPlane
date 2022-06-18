import asyncio

import aiosqlite
from discord import RawReactionActionEvent

from spyplane._metadata import __version__
from spyplane.constants import CONTROL_CHANNEL, TICK_CHANNEL, BGS_BOT_USER_ID, EMOJI_BULLSEYE, DB_PATH
from spyplane.database.systems_repository import SystemsRepository
from spyplane.services.sync_service import SyncService
from spyplane.spy_plane import bot
from spyplane.tick_detection import TickDetection


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
    print("ERROR")
    print(event)
    print(args)
    print(kwargs)


stuff_lock = asyncio.Lock()


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    emoji_bullseye = bot.get_emoji(EMOJI_BULLSEYE)
    emoji = '✅' if emoji_bullseye is None else emoji_bullseye
    if payload.channel_id!=CONTROL_CHANNEL:
        # print(f"Not the right channel {payload.channel_id}")
        return
    if payload.user_id==bot.user.id:
        # print(f"Not the right user {payload.user_id}")
        return
    if str(payload.emoji)!=str(emoji):
        print(f"Not the target emoji {payload.emoji} {emoji} {payload.emoji.name} {emoji.name}")
        return
    message = await bot.get_channel(CONTROL_CHANNEL).fetch_message(payload.message_id)
    print(f"Content: {message.content}")
    try:
        repo = SystemsRepository()
        async with aiosqlite.connect(DB_PATH) as db:
            await repo.init(db)
            system = await repo.get_system(message.content)
    except Exception as e:
        print("OnReaction: Error when fetching system from DB")
        print(e)
    await message.delete()
    try:
        await SyncService().mark_row_scout(system, payload.member.name, payload.member.id)
    except Exception as e:
        print("OnReaction: Error when updating sheet")
        print(e)


@bot.event
async def on_message(msg):
    if msg.author.id==bot.user.id:
        # Skip through, do not try to process the bots own messages or we will loop forever.
        pass
    elif msg.author.id==BGS_BOT_USER_ID and msg.channel.id==TICK_CHANNEL:
        # Route this to the tick detection handler
        TickDetection().validate_message(msg)

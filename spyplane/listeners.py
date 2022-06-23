import asyncio

from discord import RawReactionActionEvent, Message

from spyplane._metadata import __version__
from spyplane.constants import CONTROL_CHANNEL, TICK_CHANNEL, BGS_BOT_USER_ID, EMOJI_BULLSEYE, log
from spyplane.services.post_after_tick_service import PostAfterTickService
from spyplane.services.scout_recording_service import ScoutRecordingService
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
    bot.channel = bot.get_channel(CONTROL_CHANNEL)
    bot.lock = asyncio.Lock()
    emoji = bot.get_emoji(EMOJI_BULLSEYE)
    bot.emoji_bullseye = emoji or '✅'
    await bot.channel.send(f'{bot.user.name} has connected to Discord server. Version: {__version__}')


@bot.event
async def on_disconnect():
    print(f'Spy Plane has disconnected from discord server. Version: {__version__}.')


@bot.event
async def on_error(event, *args, **kwargs):
    print("ERROR")
    print(event)
    print(args)
    print(kwargs)


record = ScoutRecordingService()


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    if payload.channel_id!=CONTROL_CHANNEL:
        # print(f"Not the right channel {payload.channel_id}")
        return
    if payload.user_id==bot.user.id:
        # print(f"Not the right user {payload.user_id}")
        return
    if str(payload.emoji)!=str(bot.emoji_bullseye):
        print(f"Not the target emoji {payload.emoji} {bot.emoji_bullseye} {payload.emoji.name} {bot.emoji_bullseye.name}")
        return
    message: Message = await bot.channel.fetch_message(payload.message_id)
    asyncio.create_task(record.record_reaction(message.content, payload.member.name, payload.member.id))  # Another option is to try a Queue
    await message.delete()


@bot.event
async def on_message(msg):
    try:
        if msg.author.id==bot.user.id:
            # print("Message from bot to itself")
            pass
        elif msg.author.id==BGS_BOT_USER_ID and msg.channel.id==TICK_CHANNEL:
            log("Message from BGS Bot in tick channel!")
            await PostAfterTickService().validate_message(msg)
    except Exception as e:
        log("Exception on message")
        log(str(e))

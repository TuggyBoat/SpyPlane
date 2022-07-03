import asyncio

from discord import RawReactionActionEvent, Message

from spyplane._metadata import __version__
from spyplane.constants import CONTROL_CHANNEL, EMOJI_BULLSEYE, log, log_exception
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


post_service = PostAfterTickService()
record_service = ScoutRecordingService()


@bot.event
async def on_ready():
    log(f'{bot.user.name} has connected to Discord server. Version: {__version__}')
    bot.channel = bot.get_channel(CONTROL_CHANNEL)
    bot.lock = asyncio.Lock()
    emoji = bot.get_emoji(EMOJI_BULLSEYE)
    bot.emoji_bullseye = emoji or '✅'

    # Cron in not needed anymore, we are able to read embeds, and BGS Bot messages can trigger spy plane.
    # await bot.channel.send(f'{bot.user.name} has connected to Discord server. Version: {__version__}')
    # @aiocron.crontab('0/10 * * * *')
    # async def tick_cron_job():
    #     await post_service.tick_check_and_schedule()


@bot.event
async def on_disconnect():
    log(f'Spy Plane has disconnected from discord server. Version: {__version__}.')


@bot.event
async def on_error(event, *args, **kwargs):
    log("ERROR")
    log(event)
    log(args)
    log(kwargs)


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    try:
        if payload.channel_id!=CONTROL_CHANNEL:
            # log(f"Not the right channel {payload.channel_id}")
            return
        if payload.user_id==bot.user.id:
            # log(f"Not the right user {payload.user_id}")
            return
        if str(payload.emoji)!=str(bot.emoji_bullseye):
            log(f"Not the target emoji {payload.emoji} {bot.emoji_bullseye} {payload.emoji.name} {bot.emoji_bullseye.name}")
            return
        message: Message = await bot.channel.fetch_message(payload.message_id)
        asyncio.create_task(record_service.record_reaction(message.content, payload.member.name, payload.member.id))  # Another option is to try a Queue
        if not message.pinned:  # prevent deleting pinned messages with reactions in the channel
            await message.delete()
    except Exception as e:
        log_exception("on_raw_reaction_add", e)


@bot.event
async def on_message(msg):
    try:
        await post_service.validate_and_schedule(msg)
    except Exception as e:
        log_exception("on_message", e)

"""
The Python script that starts the bot.

"""

# import libraries
import asyncio
import os

# import build functions
from ptn.spyplane.database.database import build_database_on_startup
from ptn.spyplane.bot import bot

# import bot Cogs
from ptn.spyplane.botcommands.ModCommands import ModCommands
from ptn.spyplane.botcommands.DatabaseInteraction import DatabaseInteraction
from ptn.spyplane.botcommands.SpyPlaneCommands import SpyPlaneCommands

# import bot object, token, production status
from ptn.spyplane.constants import TOKEN, _production, DATA_DIR
from ptn.spyplane.modules.Listeners import Listeners

# import socket
from ptn.spyplane.modules.TickWebSocket import start_client

print(f"Data dir is {DATA_DIR} from {os.path.join(os.getcwd(), 'ptn', 'spyplane', DATA_DIR, '.env')}")

print(f'PTN ModBot is connecting against production: {_production}.')


def run():
    bot.add_listener(on_bot_ready, 'on_ready')
    asyncio.run(modbot())


async def modbot():
    async with bot:
        await build_database_on_startup()
        await bot.add_cog(ModCommands(bot))
        await bot.add_cog(DatabaseInteraction(bot))
        await bot.add_cog(SpyPlaneCommands(bot))
        await bot.add_cog(Listeners(bot))
        await bot.start(TOKEN)


async def on_bot_ready():
    """
    Runs socket client when the bot is ready
    """
    print('Bot is ready!')
    await start_client()  # Start the socket client when the bot is ready


if __name__ == '__main__':
    """
    If running via `python ptn/spyplane/application.py
    """
    run()

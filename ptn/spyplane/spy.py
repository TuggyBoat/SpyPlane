from ptn.spyplane.cogs.DiscordBotCommands import DiscordBotCommands
from ptn.spyplane.constants import bot, TOKEN, _production

print(f'SpyPlane is connecting against production: {_production}.')


def run():
    """
    Logic to build the bot and run the script.

    :returns: None
    """
    bot.add_cog(DiscordBotCommands(bot))
    bot.run(TOKEN)


if __name__ == '__main__':
    run()

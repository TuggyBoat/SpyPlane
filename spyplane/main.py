from spyplane.constants import TOKEN
from spyplane.spy_plane import bot
from spyplane.commands import Commands
from spyplane.listeners import Listeners


def run():
    Listeners()
    Commands()
    bot.run(TOKEN)


if __name__ == '__main__':
    run()

from spyplane.commands import Commands
from spyplane.constants import TOKEN
from spyplane.listeners import Listeners
from spyplane.spy_plane import bot


def run():
    Listeners()
    Commands()
    bot.run(TOKEN)


if __name__=='__main__':
    run()

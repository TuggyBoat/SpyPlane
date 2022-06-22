from sqlite3 import OperationalError

from aiosqlite import Connection

from spyplane.spy_plane import bot


class BaseRepository:

    def db(self) -> Connection:
        return bot.db

    @staticmethod
    async def begin():
        try:
            await bot.db.execute("BEGIN")
        except OperationalError as e:
            if str(e)=="cannot start a transaction within a transaction":
                await bot.db.execute("END TRANSACTION")
                await bot.db.execute("BEGIN")

    @staticmethod
    async def rollback():
        await bot.db.execute("ROLLBACK")

    @staticmethod
    async def commit():
        await bot.db.execute("COMMIT")

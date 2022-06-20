from aiosqlite import Connection

from spyplane.spy_plane import bot


class BaseRepository:

    def db(self) -> Connection:
        return bot.db

    @staticmethod
    async def begin():
        await bot.db.execute("BEGIN")

    @staticmethod
    async def rollback():
        await bot.db.execute("ROLLBACK")

    @staticmethod
    async def commit():
        await bot.db.execute("COMMIT")

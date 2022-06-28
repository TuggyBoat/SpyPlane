from unittest import IsolatedAsyncioTestCase

from spyplane.database.config_repository import ConfigRepository
from spyplane.spy_plane import bot


class BaseRepositoryTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        await bot.dbinit()
        self.subject = ConfigRepository()

    async def asyncTearDown(self):
        await self.subject.rollback()
        await bot.dbclose()

    async def test_record_scout(self):
        await self.subject.begin()
        await self.subject.begin()

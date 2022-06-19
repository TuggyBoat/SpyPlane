import datetime
from unittest import IsolatedAsyncioTestCase

import aiosqlite

from spyplane.constants import DB_PATH
from spyplane.database.config_repository import ConfigRepository
from spyplane.models.config import Config


class ConfigRepositoryTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.subject = ConfigRepository()

    async def test_record_scout(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await self.subject.init(db)
            await self.subject.update("interval_hours", "6", commit=False)
            c: Config = await self.subject.get_config("interval_hours")
            await self.subject.rollback()
        self.assertEqual("interval_hours", c.name)
        self.assertEqual("6", c.value)
        self.assertEqual(datetime.datetime.now(datetime.timezone.utc).date(), c.timestamp.date())

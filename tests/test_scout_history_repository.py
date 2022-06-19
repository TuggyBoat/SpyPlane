import datetime
from typing import List
from unittest import IsolatedAsyncioTestCase

import aiosqlite

from spyplane.constants import DB_PATH
from spyplane.database.scout_history_repository import ScoutHistoryRepository
from spyplane.models.scout_history import ScoutHistory
from spyplane.models.scout_system import ScoutSystem


class ScoutHistoryRepositoryTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.subject = ScoutHistoryRepository()

    async def test_record_scout(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await self.subject.init(db)
            await self.subject.record_scout(ScoutSystem('Volowahku', '1', 3), "zaszrespawned", 354990093980663889)
            history: List[ScoutHistory] = await self.subject.get_history(username="zaszrespawned")
            await self.subject.rollback()
        for scout in history:
            print(scout)
        self.assertEqual(len(history), 1)
        self.assertEqual("Volowahku", history[0].system_name)
        self.assertEqual("zaszrespawned", history[0].username)
        self.assertEqual(354990093980663889, history[0].userid)
        self.assertEqual(datetime.datetime.now(datetime.timezone.utc).date(), history[0].timestamp.date())

from unittest import IsolatedAsyncioTestCase

from spyplane.database.systems_repository import SystemsRepository
from spyplane.services.sync_service import SyncService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper
from spyplane.spy_plane import bot


class SyncServiceTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await bot.dbinit()
        self.repo = SystemsRepository()
        await self.repo.purge_scout_systems()
        self.sheets = SpreadsheetHelper(sheet='Integration Testing')
        self.subject = SyncService(self.sheets, self.repo)

    async def test_sync_systems(self):
        await self.subject.sync_db_sheet()
        systems = await self.repo.get_systems("select system_name, priority, rownum from scout_systems")
        sys_names = [s.system for s in systems]
        self.assertIn("Velas", sys_names)
        self.assertIn("Volowahku", sys_names)

    async def asyncTearDown(self):
        await bot.dbclose()

from unittest import IsolatedAsyncioTestCase

from spyplane.database.systems_repository import SystemsRepository
from spyplane.services.sync_service import SyncService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper
from spyplane.spy_plane import bot


class SyncServiceTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await bot.dbinit()
        self.repository = SystemsRepository()
        self.sheets = SpreadsheetHelper(sheet='Integration Testing')
        self.subject = SyncService(self.sheets, self.repository)

    async def test_sync_systems(self):
        await self.repository.begin()
        await self.subject.sync_db_sheet()
        await self.repository.rollback()
        self.assertTrue(True)

    async def asyncTearDown(self):
        await bot.dbclose()

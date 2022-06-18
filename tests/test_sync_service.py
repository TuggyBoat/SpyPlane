from unittest import IsolatedAsyncioTestCase

from spyplane.services.sync_service import SyncService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper


class SyncServiceTests(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.subject = SyncService()
        self.subject.sheets = SpreadsheetHelper(sheet='Integration Testing')

    async def test_sync_systems(self):
        await self.subject.sync_db_sheet(commit=False)
        self.assertTrue(True)

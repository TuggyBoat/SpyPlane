import unittest

from spyplane.services.sync_service import SyncService
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper


class SyncServiceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = SyncService()
        self.subject.sheets = SpreadsheetHelper(sheet='Integration Testing')
        self.subject.repo.begin_transaction()

    def tearDown(self) -> None:
        self.subject.repo.rollback_transaction()

    def test_sync_systems(self):
        self.subject.sync_db_sheet(commit=False)
        self.assertTrue(True)

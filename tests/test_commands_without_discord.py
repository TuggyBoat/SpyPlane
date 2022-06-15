import unittest
from typing import List

from spyplane.database.systems_repository import SystemsRepository
from spyplane.sheets.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper


class SystemsRepositoryTests(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = SystemsRepository(path='../workspace/spyplane.db')
        self.sheets = SpreadsheetHelper(sheet='Integration Testing')
        self.repo.begin_transaction()

    def tearDown(self) -> None:
        self.repo.rollback_transaction()

    def test_sync_systems(self):
        list = self.sheets.read_whole_sheet()
        self.repo.write_system_to_scout(list, commit=False)
        valid_scouts_actual: List[ScoutSystem] = self.repo.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        invalid_scouts_actual: List[ScoutSystem] = self.repo.get_invalid_systems()
        self.sheets.mark_row_invalid([system.rownum for system in invalid_scouts_actual])
        self.assertTrue(True)


if __name__=='__main__':
    unittest.main()

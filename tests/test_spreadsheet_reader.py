import unittest
from typing import List

from spyplane.sheets.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_reader import SpreadsheetReader


class SpreadsheetReaderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = SpreadsheetReader()

    def tearDown(self) -> None:
        pass

    def test_read_sheet(self):
        scout_system_list: List[ScoutSystem] = self.subject.read_whole_sheet()
        for scout in scout_system_list:
            print(scout)
        self.assertTrue("Col 285 Sector OT-G c11-6" in [scout_system.system for scout_system in scout_system_list])


if __name__=='__main__':
    unittest.main()

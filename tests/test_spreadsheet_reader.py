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
        self.assertEqual(True, True)  # TODO: add assertion here


if __name__ == '__main__':
    unittest.main()

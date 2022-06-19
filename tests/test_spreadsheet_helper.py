import unittest
from typing import List

from spyplane.models.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper, clean


class SpreadsheetReaderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = SpreadsheetHelper("Integration Testing")

    def tearDown(self) -> None:
        pass

    def test_unicode(self):
        print("HIP 64443︎".encode('unicode-escape'))
        self.assertEqual(clean("HIP 64443︎"), "HIP 64443")

    def test_read_sheet(self):
        scout_system_list: List[ScoutSystem] = self.subject.read_whole_sheet()
        for scout in scout_system_list:
            print(scout)
        self.assertTrue("Volowahku" in [scout_system.system for scout_system in scout_system_list])
        self.assertTrue("System" not in [scout_system.system for scout_system in scout_system_list])

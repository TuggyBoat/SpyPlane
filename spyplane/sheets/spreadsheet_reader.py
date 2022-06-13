from typing import List

import gspread

from spyplane.sheets.scout_system import ScoutSystem

gc = gspread.service_account(filename='/Users/zasz/repos/ptn/SpyPlane/token.json')


class SpreadsheetReader:

    def __init__(self, sheet_name: str = "Faction Scouting"):
        self.sheet_name = sheet_name

    def read_whole_sheet(self) -> List[ScoutSystem]:
        wks = gc.open(self.sheet_name).sheet1
        list_of_lists = wks.get_all_values()
        return [ScoutSystem(row[0], row[1]) for row in list_of_lists]

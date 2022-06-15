from typing import List

import gspread

from spyplane.constants import GDRIVE_TOKEN
from spyplane.sheets.scout_system import ScoutSystem

gc = gspread.service_account(filename=GDRIVE_TOKEN)


class SpreadsheetHelper:

    def __init__(self, sheet: str = "Faction Scouting"):
        self.sheet_name = sheet
        self.wks = gc.open(self.sheet_name).sheet1

    def mark_row_invalid(self, indexes: List[int]):
        for i in indexes:
            self.wks.format(f"A{i+1}:B{i+1}", {
                "backgroundColor": {
                    "red": 1.0,
                    "green": 0.8,
                    "blue": 0.8
                }
            })

    def read_whole_sheet(self) -> List[ScoutSystem]:
        list_of_lists = self.wks.get_all_values()
        ss_list = []
        for index, row in enumerate(list_of_lists):
            if row[0].strip()!="System":
                ss_list.append(ScoutSystem(row[0].strip(), row[1].strip(), index))
        return ss_list

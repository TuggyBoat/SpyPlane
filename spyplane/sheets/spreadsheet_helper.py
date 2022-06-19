import unicodedata
from typing import List

import gspread

from spyplane.constants import GDRIVE_TOKEN
from spyplane.models.scout_system import ScoutSystem

gc = gspread.service_account(filename=GDRIVE_TOKEN)


class SpreadsheetHelper:

    def __init__(self, sheet: str = "Faction Scouting"):
        self.sheet_name = sheet
        self.wks = gc.open(self.sheet_name).sheet1

    def mark_row_invalid(self, indexes: List[int]):
        for i in indexes:
            self.wks.format(f"A{i + 1}:B{i + 1}", {
                "backgroundColor": {
                    "red": 0.957,
                    "green": 0.8,
                    "blue": 0.8
                }
            })

    def mark_row_valid(self, indexes: List[int]):
        for i in indexes:
            self.wks.format(f"A{i + 1}:B{i + 1}", {
                "backgroundColor": {
                    "red": 0.85,
                    "green": 0.918,
                    "blue": 0.827
                }
            })

    def mark_row_scout(self, rownum, user_name, user_id):
        self.wks.update(f"C{rownum + 1}", [[user_name, str(user_id)]])

    def read_whole_sheet(self) -> List[ScoutSystem]:
        list_of_lists = self.wks.get_all_values()
        ss_list = []
        for index, row in enumerate(list_of_lists):
            column_a = clean(row[0])
            column_b = clean(row[1])
            if column_a!="System" and not column_a.startswith('#'):
                ss_list.append(ScoutSystem(column_a, column_b, index))
        return ss_list


def clean(s: str):
    return "".join(ch for ch in s.strip() if unicodedata.category(ch)[0] not in ["C", "M"])

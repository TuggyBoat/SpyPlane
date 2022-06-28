import unicodedata
from typing import List
from datetime import datetime
import gspread

from spyplane.constants import GDRIVE_TOKEN
from spyplane.models.scout_system import ScoutSystem

gc = gspread.service_account(filename=GDRIVE_TOKEN)


class SpreadsheetHelper:

    def __init__(self, sheet: str = "Faction Scouting"):
        self.sheet_name = sheet
        self.wks = gc.open(self.sheet_name).sheet1
        self.light_red = {
            "red": 0.957,
            "green": 0.8,
            "blue": 0.8
        }
        self.light_green = {
            "red": 0.85,
            "green": 0.918,
            "blue": 0.827
        }

    def mark_rows(self, valid: List[int], invalid: List[int]):
        formats = [{
            "range": f"A{i + 1}:B{i + 1}",
            "format": {
                "backgroundColor": self.light_green
            }
        } for i in valid] + [{
            "range": f"A{i + 1}:B{i + 1}",
            "format": {
                "backgroundColor": self.light_red
            }
        } for i in invalid]
        self.wks.batch_format(formats)

    def mark_row_scout(self, rownum, user_name, user_id, ts: datetime):
        self.wks.update(f"C{rownum + 1}", [[user_name, str(user_id), "{:%b %d %H:%M:%S}".format(ts)]])

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

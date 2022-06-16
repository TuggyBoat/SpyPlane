from typing import List

from spyplane.database.systems_repository import SystemsRepository
from spyplane.sheets.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper


class SyncService:
    def __init__(self):
        self.repo = SystemsRepository(path='./workspace/spyplane.db')
        self.sheets = SpreadsheetHelper()

    def sync_db_sheet(self, commit=True):
        scout_system_list = self.sheets.read_whole_sheet()
        self.repo.write_system_to_scout(scout_system_list, commit=commit)
        valid_scouts_actual: List[ScoutSystem] = self.repo.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        invalid_scouts_actual: List[ScoutSystem] = self.repo.get_invalid_systems()
        self.sheets.mark_row_invalid([system.rownum for system in invalid_scouts_actual])
        self.sheets.mark_row_valid([system.rownum for system in valid_scouts_actual])

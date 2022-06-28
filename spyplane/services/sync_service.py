from typing import List
from datetime import datetime
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper
from spyplane.spy_plane import bot


class SyncService:
    def __init__(self, sheets=SpreadsheetHelper(), repo=SystemsRepository()):
        self.sheets = sheets
        self.repo = repo

    async def sync_db_sheet(self):
        scout_system_list = self.sheets.read_whole_sheet()
        await self.repo.write_system_to_scout(scout_system_list)
        valid_scouts_actual: List[ScoutSystem] = await self.repo.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        invalid_scouts_actual: List[ScoutSystem] = await self.repo.get_invalid_systems()
        self.sheets.mark_rows(
            [system.rownum for system in valid_scouts_actual],
            [system.rownum for system in invalid_scouts_actual]
        )

    async def mark_row_scout(self, system: ScoutSystem, user_name, user_id, ts: datetime):
        print(f"Sheet Update: {user_name}:{user_id} scouted {system.system}.")
        await bot.loop.run_in_executor(None, self.sheets.mark_row_scout, system.rownum, user_name, user_id, ts)

from typing import List

import aiosqlite

from spyplane.constants import DB_PATH
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.scout_system import ScoutSystem
from spyplane.sheets.spreadsheet_helper import SpreadsheetHelper
from spyplane.spy_plane import bot


class SyncService:
    def __init__(self):
        self.sheets = SpreadsheetHelper()

    async def sync_db_sheet(self, commit=True):
        scout_system_list = self.sheets.read_whole_sheet()
        repo = SystemsRepository()
        async with aiosqlite.connect(DB_PATH) as db:
            await repo.init(db)
            await repo.write_system_to_scout(scout_system_list, commit=commit)
            valid_scouts_actual: List[ScoutSystem] = await repo.get_valid_systems()
            for scout in valid_scouts_actual:
                print(scout)
            invalid_scouts_actual: List[ScoutSystem] = await repo.get_invalid_systems()
            if not commit:
                await db.rollback()
        self.sheets.mark_row_invalid([system.rownum for system in invalid_scouts_actual])
        self.sheets.mark_row_valid([system.rownum for system in valid_scouts_actual])

    async def mark_row_scout(self, system: ScoutSystem, user_name, user_id):
        print(f"Sheet Update: {user_name}:{user_id} scouted {system.system}.")
        await bot.loop.run_in_executor(None, self.sheets.mark_row_scout, system.rownum, user_name, user_id)

from datetime import datetime
from spyplane.database.scout_history_repository import ScoutHistoryRepository
from spyplane.database.systems_repository import SystemsRepository
from spyplane.services.sync_service import SyncService
from spyplane.spy_plane import bot


class ScoutRecordingService:

    def __init__(self, sync=SyncService(), systems_repo=SystemsRepository(), history_repo=ScoutHistoryRepository()):
        self.sync = sync
        self.systems_repo = systems_repo
        self.history_repo = history_repo

    async def record_reaction(self, content: str, username: str, userid: int) -> None:
        try:
            print(f"Content: {content}")
            system = await self.systems_repo.get_system(content)
            async with bot.lock:
                await self.systems_repo.begin()
                ts = datetime.now()
                await self.history_repo.record_scout(system, username, userid, ts)
                await self.systems_repo.remove_scouted(system.system)
                await self.systems_repo.commit()
                print(f"Message deleted: {content}")
                await SyncService().mark_row_scout(system, username, userid, ts)
        except Exception as e:
            print("OnReaction: Error when recording the scout")
            print(e)

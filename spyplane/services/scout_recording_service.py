from discord import Message

from spyplane.database.scout_history_repository import ScoutHistoryRepository
from spyplane.database.systems_repository import SystemsRepository
from spyplane.services.sync_service import SyncService
from spyplane.spy_plane import bot


class ScoutRecordingService:

    def __init__(self, sync=SyncService(), systems_repo=SystemsRepository(), history_repo=ScoutHistoryRepository()):
        self.sync = sync
        self.systems_repo = systems_repo
        self.history_repo = history_repo

    async def record_reaction(self, message: Message, username: str, userid: int) -> None:
        try:
            print(f"Content: {message.content}")
            system = await self.systems_repo.get_system(message.content)
            async with bot.lock:
                await self.systems_repo.begin()
                await self.history_repo.record_scout(system, username, userid)
                await self.systems_repo.remove_scouted(system.system)
                await self.systems_repo.commit()
                await message.delete()
                print(f"Message deleted: {message.content}")
                await SyncService().mark_row_scout(system, username, userid)
        except Exception as e:
            print("OnReaction: Error when recording the scout")
            print(e)

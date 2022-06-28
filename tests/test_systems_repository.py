from typing import List
from unittest import IsolatedAsyncioTestCase

from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.scout_system import ScoutSystem
from spyplane.spy_plane import bot


class SystemsRepositoryTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        await bot.dbinit()
        self.subject = SystemsRepository()
        self.test_scouts = [
            ScoutSystem('', '1', 2), ScoutSystem('Velas', '1', 2),
            ScoutSystem('Velas', '1', 2), ScoutSystem('Volowahku', '1', 3),
            ScoutSystem('Vela1s', '1', 2), ScoutSystem('Wader', 'blah', 3)
        ]
        await self.subject.purge_scout_systems()

    async def asyncTearDown(self):
        await bot.dbclose()

    async def test_get_valid_systems(self):
        await self.subject.write_system_to_scout(self.test_scouts)
        valid_scouts_actual: List[ScoutSystem] = await self.subject.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        actual_systems_to_scout = [scout_system.system for scout_system in valid_scouts_actual]
        self.assertTrue("Velas" in actual_systems_to_scout)
        self.assertTrue("Volowahku" in actual_systems_to_scout)
        self.assertTrue("Vela1s" not in actual_systems_to_scout)
        self.assertTrue("Wader" not in actual_systems_to_scout)
        self.assertEqual(1, len([x for x in actual_systems_to_scout if x=="Velas"]))

    async def test_get_invalid_systems(self):
        await self.subject.write_system_to_scout(self.test_scouts)
        invalid_scouts_actual: List[ScoutSystem] = await self.subject.get_invalid_systems()
        for scout in invalid_scouts_actual:
            print(scout)
        systems_to_flag = [scout_system.system for scout_system in invalid_scouts_actual]
        self.assertTrue("Velas" not in systems_to_flag)
        self.assertTrue("Volowahku" not in systems_to_flag)
        self.assertTrue("Vela1s" in systems_to_flag)
        self.assertTrue("Wader" in systems_to_flag)
        self.assertTrue("" in systems_to_flag)

    async def test_get_system(self):
        await self.subject.write_system_to_scout(self.test_scouts)
        system: ScoutSystem = await self.subject.get_system('Velas')
        self.assertEqual("Velas", system.system)

    async def test_purge(self):
        valid = await self.subject.get_valid_systems()
        invalid = await self.subject.get_valid_systems()
        self.assertEqual(0, len(valid))
        self.assertEqual(0, len(invalid))

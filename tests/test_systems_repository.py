import unittest
from typing import List
from unittest import IsolatedAsyncioTestCase

import aiosqlite

from spyplane.constants import DB_PATH
from spyplane.database.systems_repository import SystemsRepository
from spyplane.models.scout_system import ScoutSystem


class SystemsRepositoryTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.subject = SystemsRepository()
        self.test_scouts = [
            ScoutSystem('Velas', '1', 2), ScoutSystem('Volowahku', '1', 3),
            ScoutSystem('Vela1s', '1', 2), ScoutSystem('Wader', 'blah', 3)
        ]

    async def test_get_valid_systems(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await self.subject.init(db)
            await self.subject.write_system_to_scout(self.test_scouts, commit=False)
            valid_scouts_actual: List[ScoutSystem] = await self.subject.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        actual_systems_to_scout = [scout_system.system for scout_system in valid_scouts_actual]
        self.assertTrue("Velas" in actual_systems_to_scout)
        self.assertTrue("Volowahku" in actual_systems_to_scout)
        self.assertTrue("Vela1s" not in actual_systems_to_scout)
        self.assertTrue("Wader" not in actual_systems_to_scout)

    async def test_get_invalid_systems(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await self.subject.init(db)
            await self.subject.write_system_to_scout(self.test_scouts, commit=False)
            invalid_scouts_actual: List[ScoutSystem] = await self.subject.get_invalid_systems()
        for scout in invalid_scouts_actual:
            print(scout)
        systems_to_flag = [scout_system.system for scout_system in invalid_scouts_actual]
        self.assertTrue("Velas" not in systems_to_flag)
        self.assertTrue("Volowahku" not in systems_to_flag)
        self.assertTrue("Vela1s" in systems_to_flag)
        self.assertTrue("Wader" in systems_to_flag)

    async def test_get_system(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await self.subject.init(db)
            await self.subject.write_system_to_scout(self.test_scouts, commit=False)
            system: ScoutSystem = await self.subject.get_system('Velas')
            await self.subject.rollback()
        self.assertEqual("Velas", system.system)

import unittest
from typing import List

from spyplane.database.systems_repository import SystemsRepository
from spyplane.sheets.scout_system import ScoutSystem


class SystemsRepositoryTests(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = SystemsRepository(path='../workspace/spyplane.db')
        self.subject.begin_transaction()
        self.test_scouts = [
            ScoutSystem('Velas', '1', 2), ScoutSystem('Volowahku', '1', 3),
            ScoutSystem('Vela1s', '1', 2), ScoutSystem('Wader', 'blah', 3)
        ]

    def tearDown(self) -> None:
        self.subject.rollback_transaction()

    def test_get_valid_systems(self):
        self.subject.write_system_to_scout(self.test_scouts, commit=False)
        valid_scouts_actual: List[ScoutSystem] = self.subject.get_valid_systems()
        for scout in valid_scouts_actual:
            print(scout)
        actual_systems_to_scout = [scout_system.system for scout_system in valid_scouts_actual]
        self.assertTrue("Velas" in actual_systems_to_scout)
        self.assertTrue("Volowahku" in actual_systems_to_scout)
        self.assertTrue("Vela1s" not in actual_systems_to_scout)
        self.assertTrue("Wader" not in actual_systems_to_scout)

    def test_get_invalid_systems(self):
        self.subject.write_system_to_scout(self.test_scouts, commit=False)
        invalid_scouts_actual: List[ScoutSystem] = self.subject.get_invalid_systems()
        for scout in invalid_scouts_actual:
            print(scout)
        systems_to_flag = [scout_system.system for scout_system in invalid_scouts_actual]
        self.assertTrue("Velas" not in systems_to_flag)
        self.assertTrue("Volowahku" not in systems_to_flag)
        self.assertTrue("Vela1s" in systems_to_flag)
        self.assertTrue("Wader" in systems_to_flag)


if __name__=='__main__':
    unittest.main()

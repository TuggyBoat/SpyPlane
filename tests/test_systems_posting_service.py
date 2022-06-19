import unittest
from typing import List

from spyplane.services.systems_posting_service import SystemsPostingService, split_valid_systems
from spyplane.models.scout_system import ScoutSystem


class SystemsPostingServiceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.subject = SystemsPostingService(None)

    def tearDown(self) -> None:
        pass

    def test_split_valid_systems(self):
        primary = [ScoutSystem(f"System{i}", "1", 1) for i in range(1, 5)]
        secondary: List[ScoutSystem] = [ScoutSystem(f"System{i}", "2", 1) for i in range(6, 12)]
        tertiary = [ScoutSystem(f"System{i}", "3", 1) for i in range(12, 21)]
        systems = primary + secondary + tertiary
        day_list = split_valid_systems(systems, 1)
        self.assertEqual(day_list['Secondary'], secondary[3:6])
        self.assertEqual(day_list['Tertiary'], tertiary[3:6])
        day_list = split_valid_systems(systems, 2)
        self.assertEqual(day_list['Secondary'], secondary[0:3])
        self.assertEqual(day_list['Tertiary'], tertiary[6:9])
        day_list = split_valid_systems(systems, 3)
        self.assertEqual(day_list['Secondary'], secondary[3:6])
        self.assertEqual(day_list['Tertiary'], tertiary[0:3])
        day_list = split_valid_systems(systems, 4)
        self.assertEqual(day_list['Secondary'], secondary[0:3])
        self.assertEqual(day_list['Tertiary'], tertiary[3:6])
        day_list = split_valid_systems(systems, 5)
        self.assertEqual(day_list['Secondary'], secondary[3:6])
        self.assertEqual(day_list['Tertiary'], tertiary[6:9])
        day_list = split_valid_systems(systems, 6)
        self.assertEqual(day_list['Secondary'], secondary[0:3])
        self.assertEqual(day_list['Tertiary'], tertiary[0:3])
        day_list = split_valid_systems(systems, 7)
        self.assertEqual(day_list['Secondary'], secondary[3:6])
        self.assertEqual(day_list['Tertiary'], tertiary[3:6])
        day_list = split_valid_systems(systems, 8)
        self.assertEqual(day_list['Secondary'], secondary[0:3])
        self.assertEqual(day_list['Tertiary'], tertiary[6:9])
        day_list = split_valid_systems(systems, 9)
        self.assertEqual(day_list['Secondary'], secondary[3:6])
        self.assertEqual(day_list['Tertiary'], tertiary[0:3])
        day_list = split_valid_systems(systems, 10)
        self.assertEqual(day_list['Secondary'], secondary[0:3])
        self.assertEqual(day_list['Tertiary'], tertiary[3:6])

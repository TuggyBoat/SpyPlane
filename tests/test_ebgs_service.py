from typing import List
from unittest import IsolatedAsyncioTestCase, mock
from test_data import test_data

from spyplane.services.ebgs_service import EliteBgsService


class EliteBgsServiceTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.subject = EliteBgsService()

    async def asyncTearDown(self):
        pass

    @mock.patch('aiohttp.ClientSession.get', side_effect=test_data.mocked_requests_get)
    async def test_get_system_faction_not_none_states_all_none(self, mocked_get):
        list_system_states = await self.subject.get_system_faction_not_none_states('Wally Bei')
        self.assertEqual(len(list_system_states), 0)

    @mock.patch('aiohttp.ClientSession.get', side_effect=test_data.mocked_requests_get)
    async def test_get_system_faction_not_none_states_some_interesting(self, mocked_get):
        list_system_states = await self.subject.get_system_faction_not_none_states('Beatis')
        self.assertEqual(len(list_system_states), 2)
        self.assertEqual(list_system_states[0].name, 'Verner Imperial Society')
        self.assertEqual(list_system_states[0].active, 'expansion,election')
        self.assertEqual(list_system_states[1].name, 'Allied Beatis Nationalists')
        self.assertEqual(list_system_states[1].active, 'election')

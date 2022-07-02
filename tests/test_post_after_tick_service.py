from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from spyplane.services.post_after_tick_service import PostAfterTickService


class PostAfterTickServiceTests(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.subject = PostAfterTickService(None)

    def tearDown(self) -> None:
        pass

    async def test_tick_changed(self):
        tick_check = await self.subject.tick_check()
        print(self.subject.tick_service.current_tick)
        print(self.subject.tick_service.get_current_tick())
        self.assertFalse(tick_check)
        self.assertEqual(10, len(str(self.subject.tick_service.current_tick)))
        self.assertTrue(self.subject.tick_service.get_current_tick() <= datetime.utcnow())

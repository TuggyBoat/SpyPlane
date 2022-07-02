import asyncio
import urllib
from datetime import datetime
from typing import Optional
from urllib.request import urlopen

import jq

from spyplane.constants import log

tick_query = '''
.[] | .time |= sub(".000Z";"Z") | .time | fromdateiso8601
'''


class TickService:
    def __init__(self, current_tick: Optional[int] = None):
        self.compiled_tick_date_query = jq.compile(tick_query)
        self.current_tick: int = current_tick or self.fetch_current_tick()
        log(f"Current Tick: {self.current_tick}")
        assert self.current_tick

    def get_current_tick(self) -> datetime:
        return datetime.utcfromtimestamp(int(self.current_tick))

    async def has_ticked(self) -> bool:
        new_tick = await self.async_fetch_current_tick()
        assert new_tick
        tick_changed = self.current_tick != new_tick
        if tick_changed:
            log(f'Tick detected: Current {self.current_tick}, New {new_tick}')
            self.current_tick = new_tick
        else:
            log(f'No new tick')
        return tick_changed

    async def async_fetch_current_tick(self) -> int:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.fetch_current_tick)

    # TODO: convert to aiorequest
    def fetch_current_tick(self) -> int:
        hdr = {
            'User-Agent': 'curl/7.68.0',
            'Accept': '*/*'
        }
        link = "https://elitebgs.app/api/ebgs/v5/ticks"
        req = urllib.request.Request(link, headers=hdr)
        f = urlopen(req)
        tick_text = self.compiled_tick_date_query.input(text=f.read().decode('utf-8')).text()
        return int(tick_text)

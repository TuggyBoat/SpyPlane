import aiohttp
import logging
from typing import Optional

import jq

from spyplane.constants import log

faction_active_state_query = '''
    .docs[].factions[]
    | select ((.faction_details.faction_presence.active_states|length > 0) or (.faction_details.faction_presence.pending_states|length > 0))    
    | { "Name": (.name), "Active":  (.faction_details.faction_presence.active_states | map(.state) | join(",")), "Pending":  (.faction_details.faction_presence.pending_states | map(.state) | join(",")) }
    '''

#  
class EliteBgsService:
    """
    Provides factions with interesting (not-none) states.
    """
    def __init__(self):
        self.compiled_faction_active_state_query = jq.compile(faction_active_state_query)

    async def get_system_faction_not_none_states(self, system):
        params = {
            "name": system,
            "page": 1,
            "factionDetails": "true"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://elitebgs.app/api/ebgs/v5/systems', params=params) as r:
                faction_history_json_parsed = await r.json()
        # print(faction_history_json_parsed, flush=True)
        compile_input = self.compiled_faction_active_state_query.input(faction_history_json_parsed)
        results = compile_input.all()
        faction_history = [result for result in results]
        return faction_history

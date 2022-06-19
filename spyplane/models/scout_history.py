from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScoutHistory:
    """Represents a system that was scouted by ptn faction supporter"""
    id: int
    system_name: str
    username: str
    userid: int
    timestamp: datetime

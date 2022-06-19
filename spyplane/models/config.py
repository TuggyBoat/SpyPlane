from dataclasses import dataclass
from datetime import datetime


@dataclass
class Config:
    """Represents a system that was scouted by ptn faction supporter"""
    id: int
    name: str
    value: str
    timestamp: datetime

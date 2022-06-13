from dataclasses import dataclass


@dataclass
class ScoutSystem:
    """Holds one parsed row from the google spreadsheet"""
    system: str
    priority: str

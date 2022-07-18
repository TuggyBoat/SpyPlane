from dataclasses import dataclass


@dataclass
class FactionState:
    """Holds result of jq query on response from ebgs system api call"""
    name: str
    active: str = ""
    pending: str = ""

    def short_form(self) -> str:
        short = f"{self.name} -"
        if len(self.active):
            short = f"{short} {self.active} (Active)"
        if len(self.pending):
            short = f"{short} {self.pending} (Pending)"
        return short
from dataclasses import dataclass


@dataclass
class FactionState:
    """Holds result of jq query on response from ebgs system api call"""
    name: str
    active: str = ""
    pending: str = ""

    def is_just_expansion(self) -> bool:
        return self.active == "expansion" or self.is_expansion_pending()
    
    def is_expansion_pending(self) -> bool:
        return self.pending == "expansion"
        
    def short_form(self) -> str:
        short = f"{self.name} -"
        if len(self.active):
            active_without_expansion = self.active.replace(",expansion", "").replace("expansion,", "")
            short = f"{short} {active_without_expansion} (Active)"
        if len(self.pending):
            pending_without_expansion = self.pending.replace(",expansion", "").replace("expansion,", "")
            short = f"{short} {pending_without_expansion} (Pending)"
        return short
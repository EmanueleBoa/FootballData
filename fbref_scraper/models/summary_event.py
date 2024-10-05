from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SummaryEvent:
    team_id: str
    player_id: Optional[str]
    player_name: Optional[str]
    type: str
    period: str
    minute: int

    def to_dict(self):
        return asdict(self)

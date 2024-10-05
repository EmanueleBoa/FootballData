from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ShotEvent:
    period: str
    minute: int
    team_id: str
    team_name: str
    player_id: str
    player_name: str
    xg: Optional[float]
    psxg: Optional[float]
    outcome: str
    distance: int
    body_part: str
    notes: Optional[str]

    def to_dict(self):
        return asdict(self)

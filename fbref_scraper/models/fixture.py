from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Fixture:
    match_id: Optional[str]
    round: Optional[str]
    week: Optional[int]
    date: str
    home_team_id: str
    away_team_id: str
    home_team_name: str
    away_team_name: str
    home_goals: Optional[int]
    away_goals: Optional[int]
    home_xg: Optional[float]
    away_xg: Optional[float]
    notes: Optional[str]

    def to_dict(self):
        return asdict(self)

from dataclasses import dataclass, asdict
from typing import List

from fbref_scraper.models import ShotEvent


@dataclass
class MatchShots:
    match_id: str
    shots: List[ShotEvent]

    def to_dict(self):
        return asdict(self)

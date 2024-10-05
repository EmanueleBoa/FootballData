from dataclasses import dataclass, asdict
from typing import List

from fbref_scraper.models import SummaryEvent, ShotEvent


@dataclass
class MatchReport:
    match_id: str
    match_summary: List[SummaryEvent]
    shots: List[ShotEvent]

    def to_dict(self):
        return asdict(self)

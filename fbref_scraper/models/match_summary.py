from dataclasses import dataclass, asdict
from typing import List

from fbref_scraper.models import SummaryEvent


@dataclass
class MatchSummary:
    match_id: str
    summary: List[SummaryEvent]

    def to_dict(self):
        return asdict(self)

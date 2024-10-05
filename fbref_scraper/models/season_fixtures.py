from dataclasses import dataclass, asdict
from typing import List

from fbref_scraper.models import Fixture


@dataclass
class SeasonFixtures:
    competition_id: str
    competition_name: str
    season: str
    fixtures: List[Fixture]

    def to_dict(self):
        return asdict(self)

from .config import BASE_URL, competition_name_to_id
from .parsers import FixturesParser, MatchSummaryParser
from .utils import RequestHandler


class FbRefScraper:
    def __init__(self):
        self.request_handler = RequestHandler()

    def download_fixtures(self, competition_name: str, season: str):
        competition_id = competition_name_to_id.get(competition_name)
        if competition_id is None:
            raise Exception(f'Competition {competition_name} not supported! '
                            f'Available competitions are: {list(competition_name_to_id.keys())}')
        url = f'{BASE_URL}/comps/{competition_id}/{season}/schedule/'
        html = self.request_handler.get(url)
        fixtures = FixturesParser().parse(html)
        return {
            'competition_id': competition_id,
            'competition_name': competition_name,
            'season': season,
            'fixtures': fixtures
        }

    def download_match_events(self, match_id: str):
        url = f'{BASE_URL}/matches/{match_id}/'
        html = self.request_handler.get(url)
        return MatchSummaryParser().parse(html)

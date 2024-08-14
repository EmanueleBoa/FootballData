from .exceptions import RequestError
from .parsers.fixtures import FixturesParser
from .parsers.summary import MatchSummaryParser
from .utils.request_handler import RequestHandler


class FbRefScraper:
    def __init__(self):
        self.request_handler = RequestHandler()

    def download_fixtures(self, url: str):
        try:
            html = self.request_handler.get(url)
            return FixturesParser().parse(html)
        except RequestError as e:
            pass

    def download_match_events(self, url: str):
        try:
            html = self.request_handler.get(url)
            return MatchSummaryParser().parse(html)
        except RequestError as e:
            pass

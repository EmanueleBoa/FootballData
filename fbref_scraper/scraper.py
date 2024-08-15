from .parsers import FixturesParser, MatchSummaryParser
from .utils import RequestHandler


class FbRefScraper:
    def __init__(self):
        self.request_handler = RequestHandler()

    def download_fixtures(self, url: str):
        html = self.request_handler.get(url)
        return FixturesParser().parse(html)

    def download_match_events(self, url: str):
        html = self.request_handler.get(url)
        return MatchSummaryParser().parse(html)

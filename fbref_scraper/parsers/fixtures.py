from typing import Optional, List

import bs4

from .base import BaseParser
from ..exceptions import ParseError


class FixturesParser(BaseParser):
    def parse(self, html: str) -> List[dict]:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        fixtures = self._get_raw_fixtures(soup)
        try:
            parsed_fixtures = [self._parse_fixture(fixture) for fixture in fixtures]
        except Exception as e:
            raise ParseError(f'Error while parsing fixtures: {e}')
        valid_fixtures = [fixture for fixture in parsed_fixtures if fixture is not None]
        return valid_fixtures

    @staticmethod
    def _get_raw_fixtures(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
        fixtures_table = soup.find_all('tbody')[0]
        fixtures = fixtures_table.find_all('tr')
        return fixtures

    def _parse_fixture(self, fixture: bs4.element.Tag) -> Optional[dict]:
        week = self._get_match_week(fixture)
        if week is None:
            return None
        date = self._get_match_date(fixture)
        home_team_id, home_team_name = self._get_team_info(fixture, 'home')
        away_team_id, away_team_name = self._get_team_info(fixture, 'away')
        home_goals, away_goals = self._get_scores(fixture)
        home_xg = self._get_team_xg(fixture, 'home')
        away_xg = self._get_team_xg(fixture, 'away')
        match_id = self._get_match_id(fixture)
        return {
            'match_id': match_id,
            'week': week,
            'date': date,
            'home_team_id': home_team_id,
            'away_team_id': away_team_id,
            'home_team_name': home_team_name,
            'away_team_name': away_team_name,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'home_xg': home_xg,
            'away_xg': away_xg
        }

    @staticmethod
    def _get_match_week(fixture: bs4.element.Tag) -> Optional[int]:
        week = fixture.find('th', {'data-stat': 'gameweek'}).text
        if week == '':
            return None
        return int(week)

    @staticmethod
    def _get_match_date(fixture: bs4.element.Tag) -> str:
        date = fixture.find('td', {'data-stat': 'date'}).text
        start_time = fixture.find('td', {'data-stat': 'start_time'}).text.replace(' ', '')
        return date + (start_time != '') * 'T' + start_time

    @staticmethod
    def _get_team_info(fixture: bs4.element.Tag, ground: str) -> tuple[str, str]:
        team = fixture.find('td', {'data-stat': ground + '_team'})
        team_id = team.a.get('href').split('/')[3]
        team_name = team.text
        return team_id, team_name

    @staticmethod
    def _get_scores(fixture: bs4.element.Tag) -> tuple[Optional[int], Optional[int]]:
        score = fixture.find('td', {'data-stat': 'score'}).text
        if score == '':
            return None, None
        home_goals = int(score[0])
        away_goals = int(score[2])
        return home_goals, away_goals

    @staticmethod
    def _get_team_xg(fixture: bs4.element.Tag, ground: str) -> Optional[float]:
        xg = fixture.find('td', {'data-stat': ground + '_xg'}).text
        if xg == '':
            return None
        return float(xg)

    @staticmethod
    def _get_match_report_url(fixture: bs4.element.Tag) -> Optional[str]:
        url = fixture.find('td', {'data-stat': 'match_report'}).a.get('href')
        if 'matches' in url:
            return url
        return None

    def _get_match_id(self, fixture: bs4.element.Tag) -> Optional[str]:
        url = self._get_match_report_url(fixture)
        if url is None:
            return None
        return url.split('/')[3]

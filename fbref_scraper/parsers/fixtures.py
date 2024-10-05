import logging
import re
from typing import Optional, List

import bs4

from .base import BaseParser
from .utils import get_notes
from ..models import Fixture


class FixturesParser(BaseParser):
    def parse(self, html: str) -> List[Fixture]:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        fixtures = self._get_raw_fixtures(soup)
        parsed_fixtures = []
        for fixture in fixtures:
            try:
                parsed_fixtures.append(self._parse_fixture(fixture))
            except Exception as e:
                logging.error(f'Error while parsing fixture {fixture}: {e}')
        return parsed_fixtures

    def _parse_fixture(self, fixture: bs4.element.Tag) -> Fixture:
        competition_round = self._get_round(fixture)
        week = self._get_match_week(fixture)
        date = self._get_match_date(fixture)
        home_team_id, home_team_name = self._get_team_info(fixture, 'home')
        away_team_id, away_team_name = self._get_team_info(fixture, 'away')
        home_goals, away_goals = self._get_scores(fixture)
        home_xg = self._get_team_xg(fixture, 'home')
        away_xg = self._get_team_xg(fixture, 'away')
        match_id = self._get_match_id(fixture)
        notes = self._get_notes(fixture)
        return Fixture(match_id, competition_round, week, date,
                       home_team_id, away_team_id, home_team_name, away_team_name,
                       home_goals, away_goals, home_xg, away_xg, notes)

    @staticmethod
    def _get_raw_fixtures(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
        fixtures_table = soup.find('tbody')
        fixtures = fixtures_table.find_all(lambda tag: tag.name == 'tr' and not tag.has_attr("class"))
        return fixtures

    @staticmethod
    def _get_round(fixture: bs4.element.Tag) -> Optional[str]:
        competition_round = fixture.find('th', {'data-stat': 'round'})
        if competition_round is None:
            return None
        return competition_round.text

    @staticmethod
    def _get_match_week(fixture: bs4.element.Tag) -> Optional[int]:
        week = fixture.find(re.compile("^t"), {'data-stat': 'gameweek'}).text
        if week == '':
            return None
        return int(week)

    @staticmethod
    def _get_match_date(fixture: bs4.element.Tag) -> str:
        date = fixture.find('td', {'data-stat': 'date'}).text
        start_time = fixture.find('td', {'data-stat': 'start_time'}).text.replace(' ', '')
        return f"{date}{'T' if start_time else ''}{start_time}"

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
        xg = fixture.find('td', {'data-stat': ground + '_xg'})
        if xg is None or xg.text == '':
            return None
        return float(xg.text)

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

    @staticmethod
    def _get_notes(fixture: bs4.element.Tag) -> Optional[str]:
        return get_notes(fixture)

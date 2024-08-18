import re
from typing import List, Optional, Tuple

import bs4

from .base import BaseParser


class ShotsParser(BaseParser):
    def parse(self, html: str) -> Optional[List[dict]]:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        raw_shots = self._get_raw_shots(soup)
        if raw_shots is None:
            return None
        parsed_shots = []
        for shot in raw_shots:
            parsed_shots.append(self._parse_shot(shot))
        return parsed_shots

    @staticmethod
    def _get_raw_shots(soup: bs4.BeautifulSoup) -> Optional[bs4.element.ResultSet]:
        shots_table = soup.find('table', {'id': 'shots_all'})
        if shots_table is None:
            return None
        table = shots_table.find('tbody')
        return table.find_all('tr', {'class': re.compile("^shots")})

    def _parse_shot(self, shot: bs4.element.Tag) -> dict:
        period, minute = self._get_shot_period_and_minute(shot)
        team_id, team_name = self._get_team_info(shot)
        player_id, player_name = self._get_player_info(shot)
        xg = self._get_xg(shot)
        psxg = self._get_post_shot_xg(shot)
        outcome = self._get_outcome(shot)
        distance = self._get_distance(shot)
        body_part = self._get_body_part(shot)
        notes = self._get_notes(shot)
        return {
            'period': period,
            'minute': minute,
            'team_id': team_id,
            'team_name': team_name,
            'player_id': player_id,
            'player_name': player_name,
            'xg': xg,
            'psxg': psxg,
            'outcome': outcome,
            'distance': distance,
            'body_part': body_part,
            'notes': notes
        }

    @staticmethod
    def _get_shot_period_and_minute(shot: bs4.element.Tag) -> Tuple[str, int]:
        minute_string = shot.find('th', {'data-stat': 'minute'}).text
        minutes = [int(x) for x in minute_string.split('+')]
        period = '1H' if minutes[0] <= 45 else '2H'
        minute = sum(minutes)
        return period, minute

    @staticmethod
    def _get_player_info(shot: bs4.element.Tag) -> Tuple[str, str]:
        player = shot.find('td', {'data-stat': 'player'}).find('a')
        player_name = player.text
        player_id = player.get('href').split('/')[3]
        return player_id, player_name

    @staticmethod
    def _get_team_info(shot: bs4.element.Tag) -> Tuple[str, str]:
        team = shot.find('td', {'data-stat': 'team'}).find('a')
        team_id = team.get('href').split('/')[3]
        team_name = team.text
        return team_id, team_name

    @staticmethod
    def _get_xg(shot: bs4.element.Tag) -> Optional[float]:
        xg = shot.find('td', {'data-stat': 'xg_shot'})
        if xg is None or xg.text == '':
            return None
        return float(xg.text)

    @staticmethod
    def _get_post_shot_xg(shot: bs4.element.Tag) -> Optional[float]:
        xg = shot.find('td', {'data-stat': 'psxg_shot'})
        if xg is None or xg.text == '':
            return None
        return float(xg.text)

    @staticmethod
    def _get_outcome(shot: bs4.element.Tag) -> str:
        return shot.find('td', {'data-stat': 'outcome'}).text.lower().replace(' ', '_')

    @staticmethod
    def _get_distance(shot: bs4.element.Tag) -> int:
        return int(shot.find('td', {'data-stat': 'distance'}).text)

    @staticmethod
    def _get_body_part(shot: bs4.element.Tag) -> str:
        return shot.find('td', {'data-stat': 'body_part'}).text.lower().replace(' ', '_')

    @staticmethod
    def _get_notes(shot: bs4.element.Tag) -> Optional[str]:
        notes = shot.find('td', {'data-stat': 'notes'})
        if notes is None or notes.text == '':
            return None
        return notes.text.lower().replace(' ', '_')

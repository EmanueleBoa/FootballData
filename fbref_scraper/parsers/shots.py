import logging
import re
from typing import List, Optional, Tuple

import bs4

from .base import BaseParser
from .utils import get_period_and_minute, get_entity_id_and_name, get_notes
from ..models import ShotEvent


class ShotsParser(BaseParser):
    def parse(self, html: str) -> Optional[List[ShotEvent]]:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        raw_shots = self._get_raw_shots(soup)
        if raw_shots is None:
            return None
        parsed_shots = []
        for shot in raw_shots:
            try:
                parsed_shots.append(self._parse_shot(shot))
            except Exception as e:
                logging.error(f'Error while parsing shot event {shot}: {e}')
        return parsed_shots

    def _parse_shot(self, shot: bs4.element.Tag) -> ShotEvent:
        period, minute = self._get_shot_period_and_minute(shot)
        team_id, team_name = self._get_team_info(shot)
        player_id, player_name = self._get_player_info(shot)
        xg = self._get_xg(shot)
        psxg = self._get_post_shot_xg(shot)
        outcome = self._get_outcome(shot)
        distance = self._get_distance(shot)
        body_part = self._get_body_part(shot)
        notes = self._get_notes(shot)
        return ShotEvent(period, minute, team_id, team_name, player_id, player_name,
                         xg, psxg, outcome, distance, body_part, notes)

    @staticmethod
    def _get_raw_shots(soup: bs4.BeautifulSoup) -> Optional[bs4.element.ResultSet]:
        shots_table = soup.find('table', {'id': 'shots_all'})
        if shots_table is None:
            return None
        table = shots_table.find('tbody')
        return table.find_all('tr', {'class': re.compile("^shots")})

    @staticmethod
    def _get_shot_period_and_minute(shot: bs4.element.Tag) -> Tuple[str, int]:
        minute_string = shot.find('th', {'data-stat': 'minute'}).text
        return get_period_and_minute(minute_string)

    @staticmethod
    def _get_player_info(shot: bs4.element.Tag) -> Tuple[str, str]:
        player = shot.find('td', {'data-stat': 'player'}).find('a')
        return get_entity_id_and_name(player)

    @staticmethod
    def _get_team_info(shot: bs4.element.Tag) -> Tuple[str, str]:
        team = shot.find('td', {'data-stat': 'team'}).find('a')
        return get_entity_id_and_name(team)

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
        notes = get_notes(shot)
        if notes is None:
            return None
        return notes.lower().replace(' ', '_')

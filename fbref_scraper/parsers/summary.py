from typing import Optional, List

import bs4

from .base import BaseParser
from ..exceptions import ParseError


class MatchSummaryParser(BaseParser):
    def parse(self, html: str) -> List[dict]:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        raw_events = self._get_raw_events(soup)
        try:
            parsed_events = [self._parse_event(event) for event in raw_events]
        except Exception as e:
            raise ParseError(f'Error while parsing match summary: {e}')
        valid_events = [event for event in parsed_events if event is not None]
        return valid_events

    @staticmethod
    def _get_raw_events(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
        match_summary = soup.find('div', {'id': 'events_wrap'})
        return match_summary.find_all('div', class_='event')

    def _parse_event(self, event) -> Optional[dict]:
        period, minute = self._get_event_period_and_minute(event)
        event_type = self._get_event_type(event)
        team_id = self._get_team_id(event)
        player_id, player_name = self._get_player_info(event)
        if player_id is None:
            return None
        return {
            'team_id': team_id,
            'player_id': player_id,
            'player_name': player_name,
            'type': event_type,
            'period': period,
            'minute': minute
        }

    @staticmethod
    def _get_event_type(event: bs4.element.Tag) -> str:
        return event.find('div', class_='event_icon')['class'][1]

    @staticmethod
    def _get_team_id(event: bs4.element.Tag) -> str:
        return event.find('img')['src'].split('/')[-1].split('.')[0]

    @staticmethod
    def _get_event_period_and_minute(event: bs4.element.Tag) -> tuple[str, int]:
        minute_string = event.find('div').text.split('\n')[1].replace('\t', '').replace('\xa0', '').replace('’', '')
        minutes = [int(x) for x in minute_string.split('+')]
        period = '1H' if minutes[0] <= 45 else '2H'
        minute = sum(minutes)
        return period, minute

    @staticmethod
    def _get_player_info(event: bs4.element.Tag) -> tuple[Optional[str], Optional[str]]:
        player = event.find('a')
        if player is None:
            return None, None
        player_name = player.text
        player_id = player.get('href').split('/')[3]
        return player_id, player_name

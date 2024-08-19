from typing import Tuple

import bs4

FIRST_HALF = '1H'
SECOND_HALF = '2H'


def get_period_and_minute(minute_string: str) -> Tuple[str, int]:
    minutes = [int(x) for x in minute_string.split('+')]
    period = FIRST_HALF if minutes[0] <= 45 else SECOND_HALF
    minute = sum(minutes)
    return period, minute


def get_entity_id_and_name(entity: bs4.element.Tag) -> Tuple[str, str]:
    entity_id = entity.get('href').split('/')[3]
    entity_name = entity.text
    return entity_id, entity_name

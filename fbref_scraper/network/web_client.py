import logging
import time

import requests
from requests import HTTPError, ConnectionError, Timeout, RequestException

from ..exceptions import RequestError


class WebClient:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 3.):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str) -> str:
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.text

            except (HTTPError, ConnectionError, Timeout) as e:
                retries += 1
                logging.warning(f'Retry {retries} for URL: {url}. Error: {e}')

                if retries > self.max_retries:
                    raise RequestError(f'Failed to retrieve data from {url} after {self.max_retries} attempts') from e

                sleep_time = self.backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)

            except RequestException as e:
                raise RequestError(f'Request failed due to a non-retryable error: {str(e)}') from e

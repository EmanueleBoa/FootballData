import requests as requests

from ..exceptions import RequestError


class RequestHandler:
    @staticmethod
    def get(url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise RequestError(f"Request {url} failed: {str(e)}")

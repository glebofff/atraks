import urllib
from typing import Optional

from django.apps import AppConfig


class RsPlanConfig(AppConfig):
    name = 'rs_plan'
    base_url = 'https://rossvyaz.ru/data/'
    prefixes = ['3', '4', '8', '9']
    delimiter = ';'

    @classmethod
    def get_file_url(cls, url: str = None, prefix: str = None) -> Optional[str]:
        if prefix not in cls.prefixes:
            return None
        url = url or cls.base_url
        zone = 'DEF' if prefix == '9' else 'ABC'
        return urllib.parse.urljoin(
            url,
            f'{zone}-{prefix}xx.csv'
        )

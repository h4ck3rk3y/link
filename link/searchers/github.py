from .base_searcher import BaseSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from datetime import timedelta

"""
base model of the github searcher
construct request and validate are shared!
"""


class Github(BaseSearcher):
    source = "github"

    def __init__(self, token, username, query, per_page, source_result, name, url):
        self.url = url
        super().__init__(token, username, query, per_page, source_result, name)

    def construct_request(self, page=0, user_only=False) -> grequests.AsyncRequest:
        self.current_page = page
        payload = {"q": self.query,
                   "page": page, "per_page": self.per_page}
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return grequests.get(url=self.url, params=payload, hooks={'response': [self.validate_and_parse]}, headers=headers)

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            response = response.json()
            if response['message'].startswith('API rate limit exceeded'):
                banned_until = datetime.now() + timedelta(seconds=60)
            return False, banned_until
        return True, banned_until

from .base_searcher import BaseSearcher
import grequests
from datetime import datetime
from datetime import timedelta

"""
base model of the github searcher
construct request and validate are shared!

https://docs.github.com/en/rest/reference/search
for authenticated requests github allows 30 queries / minute
for unauthenticated requests github allows 10 queries / minute
"""


class Github(BaseSearcher):
    source = "github"

    def __init__(self, token, username, query, per_page, source_result, name, url):
        self.url = url
        super().__init__(token, username, query, per_page, source_result, name)

    def construct_request(self, page=0, user_only=False) -> grequests.AsyncRequest:
        payload = {"q": self.query,
                   "page": page, "per_page": self.per_page}
        headers = {"Accept": "application/vnd.github.v3+json"}
        if type(self.token) == str and len(self.token) > 0:
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

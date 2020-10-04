from .base_searcher import BaseSearcher
from datetime import datetime
from datetime import timedelta
from .constants import GITHUB_QUALIFIERS

"""
base model of the github searcher
construct request and validate are shared!

https://docs.github.com/en/rest/reference/search
for authenticated requests github allows 30 queries / minute
for unauthenticated requests github allows 10 queries / minute
"""


class GithubSearcher(BaseSearcher):
    source = "github"

    def __init__(self, token, username, query, per_page, source_result, name, url):
        self.url = url
        super().__init__(token, username, query, per_page,
                         source_result, name, acceptable_qualifiers=GITHUB_QUALIFIERS)

    def construct_request_parts(self, page, user_only):
        payload = {"q": self.query,
                   "page": page, "per_page": self.per_page}
        headers = {"Accept": "application/vnd.github.v3+json"}
        if type(self.token) == str and len(self.token) > 0:
            headers["Authorization"] = f"token {self.token}"
        if user_only:
            payload["q"] = f"{payload['q']}+user:{self.username}"
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            response = response.json()
            if response['message'].startswith('API rate limit exceeded'):
                banned_until = datetime.now() + timedelta(seconds=60)
            return False, banned_until
        return True, banned_until

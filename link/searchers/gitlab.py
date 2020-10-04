from .base_searcher import BaseSearcher
from datetime import datetime
from datetime import timedelta

"""
base model of the gitlab searcher
construct request and validate are shared!

https://docs.gitlab.com/ee/api/search.html

GitLab.com responds with HTTP status code 429 to 
requests at protected paths that exceed 10 requests per minute per IP address.
"""


class GitlabSearcher(BaseSearcher):

    def __init__(self, token, username, query, per_page, source_result, name, url, user_only):
        self.url = url
        super().__init__(token, username, query, per_page, source_result, name, user_only)

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers["Retry-After"])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

from .base_searcher import BaseSearcher
import grequests
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import ISSUE
from datetime import timedelta
import re


"""
for searches stack overflow allows about 300 searches
without api token per day.
with a token that limit is up to 10,000

in so the searches can't be personalized

"""


class Searcher(BaseSearcher):

    source = "github"
    url = "https://api.github.com/search/issues"
    name = "github_issues"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page, source_result, self.source)

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

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            link = item['html_url']
            preview = item["body"]
            title = item["title"]

            created_at = datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            single_result = SingleResult(
                preview, link, Searcher.source, created_at, ISSUE, title)
            result_page.add(single_result)
        return result_page

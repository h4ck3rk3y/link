from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import QUESTION
from datetime import timedelta
import re


"""
for searches stack overflow allows about 300 searches
without api token per day.
with a token that limit is up to 10,000

in so the searches can't be personalized

"""


class StackoverflowSearcher(BaseSearcher):

    source = "stackoverflow"
    url = "https://api.stackexchange.com/2.2/search"
    name = "stackoverflow"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page, source_result, self.name)

    def construct_request_parts(self, page, user_only):
        payload = {"intitle": self.query, "site": self.source,
                   "page": page, "pagesize": self.per_page}
        if user_only and len(self.username) > 0:
            payload["user"] = self.username
        return self.url, payload, None

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            response = response.json()
            if response['error_message'].startswith('too many requests from this IP'):
                banned_seconds = self.parse_time_from_message(
                    response['error_message'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            preview = self.generate_preview(item)
            title = item['title']
            link = item['link']
            date = datetime.fromtimestamp(item['creation_date'])
            single_result = SingleResult(
                preview, link, self.source, date, QUESTION, title)
            result_page.add(single_result)
        return result_page

    @ staticmethod
    def generate_preview(item):
        return f"This question has been viewed {item['view_count']} times and has {item['answer_count']} answers"

    @ staticmethod
    def parse_time_from_message(message):
        pattern = re.compile("\\d+")
        result = pattern.search(message)
        return int(result.group(0))

from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import MESSAGE
from datetime import timedelta
import re


"""
Documentation: https://api.slack.com/methods/search.messages
At the time of writing slack api didn't support filteirng by date.

Slack allows atleast 20 requests per minute
Search is tier 2
https://api.slack.com/docs/rate-limits#tier_t2
"""


class SlackSearcher(BaseSearcher):

    source = "slack"
    url = "https://slack.com/api/search.messages"
    name = "slack"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page, source_result, self.name)

    def construct_request_parts(self, page, user_only):
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = {"token": self.token,
                   "query": self.query, "count": self.per_page, "page": page}
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200 or not response.json()['ok']:
            if response.status_code == 429:
                banned_seconds = int(response.headers['Retry-After'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        if 'messages' not in response or 'matches' not in response['messages']:
            return result_page
        for message in response["messages"]["matches"]:
            preview = message["text"]
            title = f"Message from {message.get('username', 'unknown')} on #{message['channel']['name']}"
            link = message['permalink']
            date = datetime.fromtimestamp(float(message['ts']))
            single_result = SingleResult(
                preview, link, self.source, date, MESSAGE, title)
            result_page.add(single_result)
        return result_page

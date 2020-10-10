from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import FILE, FOLDER, WEB_LINK, BOX_TIME_FORMAT
from datetime import timedelta
import re


"""
Documentation: https://api.slack.com/methods/search.messages
At the time of writing slack api didn't support filteirng by date.

Slack allows atleast 20 requests per minute
Search is tier 2
https://api.slack.com/docs/rate-limits#tier_t2
"""


class BoxSearcher(BaseSearcher):

    source = "box"
    url = "https://api.box.com/2.0/search/"
    name = "box"
    user_priority = False

    def __init__(self, token, username, query, per_page, source_result, user_only):
        super().__init__(token, username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Content-type": "application/json"}
        headers["Authorization"] = self.token
        payload = {
            "query": self.token, "limit": self.per_page, "offset": page*self.per_page
        }
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers['retry-after'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        for entry in response["entries"]:
            preview = entry["description"]
            title = entry["name"]
            link = entry["shared_link"]["url"]
            date = datetime.strptime(entry["created_at"], BOX_TIME_FORMAT)
            assert(entry["type"] in {FILE, FOLDER, WEB_LINK})
            single_result = SingleResult(
                preview, link, self.source, date, entry["type"], title)
            result_page.add(single_result)
        return result_page

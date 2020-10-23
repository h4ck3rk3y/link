from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import TASK
from datetime import timedelta
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs


"""
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_search?view=odsp-graph-online
"""


class MicrosoftOneDriveSearcher(BaseSearcher):

    source = "microsoft"
    url = "https://graph.microsoft.com/v1.0/me/drive/search(q='%s')"
    name = "onedrive"
    user_priority = False

    def __init__(self, token, username, query, per_page, source_result, user_only):
        self.skip_token = None
        self.url = self.url % query
        super().__init__(token, username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json"}
        headers["Authorization"] = f"bearer {self.token}"
        payload = {
            "$top":  self.per_page
        }
        if self.skip_token:
            payload["$skipToken"] = self.skip_token
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers['Retry-After'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        if "@odata.nextLink" in response:
            self.skip_token = get_skip_token(response["@odata.nextlink"])
        else:
            self.skip_token = None
        for task in response["data"]:
            link = "url"
            title = task["name"]
            preview = "preview"
            single_result = SingleResult(preview=preview, link=link, source=self.source,
                                         date=None, category=TASK, title=title)
            result_page.add(single_result)
        return result_page


def get_skip_token(url):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed)['$skipToken'], True

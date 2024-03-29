from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import WIKI, ATLASSIAN_FORMAT
from datetime import timedelta
import urllib.parse as urlparse
from urllib.parse import parse_qs


"""
https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/

have tested pagination
"""


class ConfluenceSearcher(BaseSearcher):

    source = "atlassian"
    name = "confluence"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        self.atlassian_instance = user_token.extra_data["url"]
        self.cursor = None
        self.url = f"https://api.atlassian.com/ex/confluence/{user_token.extra_data['cloudId']}/wiki/rest/api/search"
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        payload = {
            "cql": f'text ~ "{self.query}"',
            "limit": self.per_page,
        }
        if self.cursor:
            payload["cursror"] = self.cursor
            payload["next"] = True
            payload["start"] = self.per_page*(page-1)
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
        if "_links" in response and "next" in response["_links"]:
            self.cursor = get_cursor(response["_links"]["next"])
        else:
            self.cursor = None
        result_page = Page()
        for wiki in response["results"]:
            preview = clean_text(wiki["excerpt"])
            title = wiki["title"]
            link = get_url(self.atlassian_instance, wiki["content"]["_links"]["webui"])
            date = datetime.strptime(wiki["lastModified"], ATLASSIAN_FORMAT)
            single_result = SingleResult(preview, link, self.source, date, WIKI, title)
            result_page.add(single_result)
        return result_page


def clean_text(text):
    return text.replace("@@@hl@@@", "").replace("@@@endhl@@@", "")


def get_url(url, path):
    return url + "/wiki" + path


def get_cursor(url):
    parsed = urlparse.urlparse(url).query
    return parse_qs(parsed)['cursor'][0]

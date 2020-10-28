from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE
from datetime import timedelta
from base64 import b64encode

"""
https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
"""


class JiraSearcher(BaseSearcher):

    source = "atlassian"
    name = "jira"
    user_priority = False

    def __init__(self, token, username, query, per_page, source_result, user_only):
        self.url = username
        super().__init__(token, username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json"}
        headers["Authorization"] = get_auth_header(self.token)
        payload = {
            "jql": f"text ~ {self.query}",
            "maxResults": self.per_page,
            "startAt": self.per_page*(page-1)
        }
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
        for issue in response["issues"]:
            preview = f"An issue in the {issue['project']['name']} project"
            title = issue["description"]
            link = issue["self"]
            date = None
            single_result = SingleResult(preview, link, self.source, date, ISSUE, title)
            result_page.add(single_result)
        return result_page


def get_auth_header(token):
    b64_encoded_user_pass = b64encode(f"{token}").decode("ascii")
    return f"Basic {b64_encoded_user_pass}"

from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE, ATLASSIAN_FORMAT
from datetime import timedelta
from base64 import b64encode

"""
https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
"""


class JiraSearcher(BaseSearcher):

    source = "atlassian"
    name = "jira"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        self.atlassian_instance = user_token.extra_data["url"]
        self.url = f"https://api.atlassian.com/ex/jira/{user_token.extra_data['cloudId']}/rest/api/2/search"
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        payload = {
            "jql": f'text ~ "{self.query}"',
            "maxResults": self.per_page,
            "startAt": self.per_page*(page-1),
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
            preview = f"An issue in the {issue['fields']['project']['name']} project"
            title = issue['fields']['summary']
            link = get_link(self.atlassian_instance, key)
            date = datetime.strptime(issue['fields']['created'], ATLASSIAN_FORMAT)
            single_result = SingleResult(preview, link, self.source, date, ISSUE, title)
            result_page.add(single_result)
        return result_page


def get_link(url, key):
    return url + "/browse" + key

from .gitlab import GitlabSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE, TRELLO_GITLAB_TIME_FORMAT
from datetime import timedelta
import os


class GitlabIssueSearcher(GitlabSearcher):

    source = "gitlab"
    name = "gitlab_issues"
    url = os.getenv("GITLAB_ISSUES_DOMAIN", "https://gitlab.com/api/v4/issues")
    user_priority = True

    def __init__(self, token, username, query, per_page, source_result, user_only):
        super().__init__(token, username, query, per_page,
                         source_result, self.name, self.url, user_only)

    def construct_request_parts(self, page):
        payload = {"search": self.query,
                   "per_page": self.per_page, "page": page, "access_token": self.token, "in": "title"}
        if not self.user_only:
            payload["scope"] = "all"
        return self.url, payload, None

    def parse(self, response):
        result_page = Page()
        for item in response:
            link = item["web_url"]
            preview = item["description"]
            title = item["title"]
            created_at = datetime.strptime(
                item["created_at"], TRELLO_GITLAB_TIME_FORMAT)
            single_result = SingleResult(
                preview=preview, link=link, source=self.source, date=created_at, category=ISSUE, title=title)
            result_page.add(single_result)
        return result_page

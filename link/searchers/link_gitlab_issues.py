from .gitlab import GitlabSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE, TRELLO_GITLAB_TIME_FORMAT
from datetime import timedelta


class GitlabIssueSearcher(GitlabSearcher):

    source = "gitlab"
    name = "gitlab_issues"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page,
                         source_result, self.name, "issues")

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

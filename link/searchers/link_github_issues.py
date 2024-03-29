from .github import GithubSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE, GITHUB_TIME_FORMAT
from datetime import timedelta
import os


class GithubIssueSearcher(GithubSearcher):

    source = "github"
    url = "https://api.github.com/search/issues"
    name = "github_issues"
    user_priority = True

    def __init__(self, user_token, query, per_page, source_result, user_only):
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, self.url, user_only)

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            link = item['html_url']
            preview = item["body"]
            title = item["title"]

            created_at = datetime.strptime(
                item["created_at"], GITHUB_TIME_FORMAT)

            single_result = SingleResult(
                preview, link, self.source, created_at, ISSUE, title, score=item['score'])
            result_page.add(single_result)
        return result_page

from .github import GithubSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import REPO, GITHUB_TIME_FORMAT
from datetime import timedelta
import os


class GithubRepoSearcher(GithubSearcher):

    source = "github"
    url = "https://api.github.com/search/repositories"
    name = "github_repos"
    user_priority = True

    def __init__(self, user_token, query, per_page, source_result, user_only):
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, self.url, user_only)

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            link = item['html_url']
            preview = item["description"]
            title = item["full_name"]

            created_at = datetime.strptime(
                item["created_at"], GITHUB_TIME_FORMAT)

            single_result = SingleResult(
                preview, link, self.source, created_at, REPO, title, score=item['score'])
            result_page.add(single_result)
        return result_page

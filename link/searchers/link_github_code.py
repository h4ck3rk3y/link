from .github import GithubSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import CODE
from datetime import timedelta


class GithubCodeSearcher(GithubSearcher):

    source = "github"
    url = "https://api.github.com/search/code"
    name = "github_code"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page,
                         source_result, self.name, self.url)

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            link = item['html_url']
            preview = item["path"]
            title = item["name"]

            # for code created_at is undefined
            created_at = None

            single_result = SingleResult(
                preview, link, self.source, created_at, CODE, title, score=item['score'])
            result_page.add(single_result)
        return result_page

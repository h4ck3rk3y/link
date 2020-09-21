from .github import GithubSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE, GITHUB_TIME_FORMAT
from datetime import timedelta


class Searcher(GithubSearcher):

    source = "github"
    url = "https://api.github.com/search/issues"
    name = "github_issues"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page,
                         source_result, Searcher.name, Searcher.url)

    def parse(self, response):
        result_page = Page()
        for item in response['items']:
            link = item['html_url']
            preview = item["body"]
            title = item["title"]

            created_at = datetime.strptime(
                item["created_at"], GITHUB_TIME_FORMAT)

            single_result = SingleResult(
                preview, link, Searcher.source, created_at, ISSUE, title, score=item['score'])
            result_page.add(single_result)
        return result_page

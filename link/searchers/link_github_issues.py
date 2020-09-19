from .github import Github
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE
from datetime import timedelta


"""
for searches stack overflow allows about 300 searches
without api token per day.
with a token that limit is up to 10,000

in so the searches can't be personalized

"""


class Searcher(Github):

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
                item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            single_result = SingleResult(
                preview, link, Searcher.source, created_at, ISSUE, title)
            result_page.add(single_result)
        return result_page

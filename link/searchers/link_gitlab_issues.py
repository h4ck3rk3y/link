from .gitlab import Gitlab
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import ISSUE
from datetime import timedelta


class Searcher(Gitlab):

    source = "gitlab"
    name = "gitlab_issues"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page,
                         source_result, Searcher.name, "issues")

    def parse(self, response):
        result_page = Page()
        for item in response:
            link = item["web_url"]
            preview = item["description"]
            title = item["title"]
            created_at = datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            single_result = SingleResult(
                preview=preview, link=link, source=Searcher.source, date=created_at, category=ISSUE, title=title)
            result_page.add(single_result)
        return result_page

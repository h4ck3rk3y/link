from .gitlab import GitlabSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import REPO
from datetime import timedelta


class Searcher(GitlabSearcher):

    source = "gitlab"
    name = "gitlab_projects"

    def __init__(self, token, username, query, per_page, source_result):
        super().__init__(token, username, query, per_page,
                         source_result, Searcher.name, "projects")

    def parse(self, response):
        result_page = Page()
        for item in response:
            link = item["web_url"]
            preview = item["description"]
            title = item["path_with_namespace"]
            created_at = datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            single_result = SingleResult(
                preview=preview, link=link, source=Searcher.source, date=created_at, category=REPO, title=title)
            result_page.add(single_result)
        return result_page

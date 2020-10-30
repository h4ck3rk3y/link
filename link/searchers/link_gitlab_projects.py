from .gitlab import GitlabSearcher
import grequests
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import REPO, TRELLO_GITLAB_TIME_FORMAT
from datetime import timedelta
import os


class GitlabProjectSearcher(GitlabSearcher):

    source = "gitlab"
    name = "gitlab_projects"
    url = "https://gitlab.com/api/v4/projects"
    user_priority = True

    def __init__(self, user_token, query, per_page, source_result, user_only):
        if "url" in user_token.extra_data:
            self.url = user_token.extra_data["url"] + "/api/v4/projects"
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, self.url, user_only)

    def construct_request_parts(self, page):
        payload = {"search": self.query,
                   "per_page": self.per_page, "page": page, "access_token": self.token}
        if self.user_only:
            payload["owned"] = True
        return self.url, payload, None

    def parse(self, response):
        result_page = Page()
        for item in response:
            link = item["web_url"]
            preview = item["description"]
            title = item["path_with_namespace"]
            created_at = datetime.strptime(
                item["created_at"], TRELLO_GITLAB_TIME_FORMAT)
            single_result = SingleResult(
                preview=preview, link=link, source=self.source, date=created_at, category=REPO, title=title)
            result_page.add(single_result)
        return result_page

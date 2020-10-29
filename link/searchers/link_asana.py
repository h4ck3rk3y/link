from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from datetime import datetime
from .constants import TASK
from datetime import timedelta
import requests


"""
Need to get a workspace GET /workspaces

Then need to use the advanced task search feature

GET /workspaces/{workspace_gid}/tasks/search

I am searching the first work space by default

https://developers.asana.com/docs/search-tasks-in-a-workspace
"""


class AsanaSearcher(BaseSearcher):

    source = "asana"
    url = "https://app.asana.com/api/1.0/workspaces/%s/tasks/search"
    name = "asana"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        workspace, workspace_name = AsanaSearcher.get_workspace(user_token.token)
        self.url = self.url % (workspace)
        self.workspace_name = workspace_name
        self.offset = None
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        payload = {
            "text": self.query, "limit": self.per_page
        }
        if self.offset:
            payload["offset"] = self.offset
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers['Retry-After'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        if "next_page" in response:
            self.offset = response["next_page"]["offset"]
        else:
            self.offset = None
        for task in response["data"]:
            link = AsanaSearcher.get_url(task["gid"])
            title = task["name"]
            preview = f"A task  in the {self.workspace_name} workspace"
            single_result = SingleResult(preview=preview, link=link, source=self.source,
                                         date=None, category=TASK, title=title)
            result_page.add(single_result)
        return result_page

    @staticmethod
    def get_url(task_id):
        return f"https://app.asana.com/0/0/{task_id}"

    @staticmethod
    def get_workspace(token):
        response = requests.get("https://app.asana.com/api/1.0/workspaces", headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        })
        if response.status_code != 200:
            return -1, ""
        return response.json()["data"][0]["gid"], response.json()["data"][0]["name"]

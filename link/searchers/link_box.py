from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import FILE, FOLDER, WEB_LINK, BOX_TIME_FORMAT
from datetime import timedelta
import re
import requests
import os

"""
At the moment the links are constructed assuming
standard box not enterprise box.

https://developer.box.com/reference/get-search/
"""

BOX_URL = "https://app.box.com"


class BoxSearcher(BaseSearcher):

    source = "box"
    url = "https://api.box.com/2.0/search/"
    name = "box"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        self.user_id = ""
        if user_only:
            self.user_id = BoxSearcher.get_user_id(user_token.token)
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Content-type": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        payload = {
            "query": self.query, "limit": self.per_page, "offset": (page-1)*self.per_page
        }
        if self.user_only and self.user_id != "":
            payload["owner_user_ids"] = f"{self.user_id}"
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers['retry-after'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        for entry in response["entries"]:
            preview = entry["description"]
            title = entry["name"]
            link = BoxSearcher.parse_path(entry["path_collection"])
            date = datetime.strptime(entry["created_at"], BOX_TIME_FORMAT)
            assert(entry["type"] in [FILE, FOLDER, WEB_LINK])
            single_result = SingleResult(
                preview, link, self.source, date, entry["type"], title)
            result_page.add(single_result)
        return result_page

    @staticmethod
    def parse_path(path_collection):
        entry = path_collection["entries"][-1]
        return f"{BOX_URL}/folder/{entry['id']}"

    @staticmethod
    def get_user_id(token):
        user_api = "https://api.box.com/2.0/users/me"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(user_api, headers=headers)
        if response.status_code == 200:
            return response.json()["id"]
        else:
            return ""

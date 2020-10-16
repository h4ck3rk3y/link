from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import FILE, FOLDER, WEB_LINK, BOX_TIME_FORMAT
from datetime import timedelta
import re
import requests

import logging
logger = logging.getLogger(__name__)

"""
API reference: https://developers.google.com/drive/api/v3/reference/files/list
"""


class GDriveSearcher(BaseSearcher):

    source = "google"
    url = "https://www.googleapis.com/drive/v3/files"
    name = "gdrive"
    user_priority = False

    def __init__(self, token, username, query, per_page, source_result, user_only):
        self.page_token = ""
        super().__init__(token, username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Content-type": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        payload = {
            "q": form_google_query(self.query),
            "pageSize": self.per_page,
            "corpora": "user",
        }
        if self.page_token:
            payload["pageToken"] = self.page_token

        if self.user_only and self.user_id != "":
            payload["owner_user_ids"] = f"{self.user_id}"
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 403:
                banned_seconds = int(response.headers['retry-after'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        if response['incompleteSearch']:
            logger.warning(f"Last search was incomplete. response: {response}")
        self.page_token = response["nextPageToken"]

        result_page = Page()
        for entry in response["files"]:
            preview = entry["description"]
            title = entry["name"]
            link = entry["webViewLink"]
            date = datetime.fromisoformat(entry["createdTime"])
            logger.info(entry)
            single_result = SingleResult(
                preview, link, self.source, date, "", title)
            result_page.add(single_result)
        return result_page


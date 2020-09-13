from .search import Search
from ..models.results import Page, SingleResult
import requests
import base64
from datetime import datetime
from datetime import timedelta
from .constants import ISSUE, MERGE_REQUESTS, REPO
import logging
import random

GITLAB_URL = "https://gitlab.example.com/api/v4/search"

SOURCENAME = "gitlab"

"""
https://docs.gitlab.com/ee/api/search.html

GitLab.com responds with HTTP status code 429 to POST requests at protected paths that exceed 10 requests per minute per IP address.
"""

CATEGORYY_MAP = {
    "projects": REPO,
    "issues": ISSUE,
    "merge_requests": MERGE_REQUESTS
}

logger = logging.getLogger(__name__)


class Gitlab(Search):

    def __init__(self, user=None):
        self.__number_of_items = 0
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return Github(user)

    def fetch(self, page=0):
        assert(self._query != None and self.query !=
               ""), "Query cannot be empty"

        if self.__number_of_items >= page*self._pagesize:
            logger.info(
                f"we already seem to have enough results: {self.__number_of_items}, not searching for more")
            return

        status, timelimit = self.rate_limit_exceeded()
        if status:
            logger.warning(
                f"Rate limit has been exceeded, try after {timelimit}")
            return

        payload = {"search": f"{self._query}"}

        if self._pagesize:
            payload['per_page'] = self._pagesize

        if page:
            payload['page'] = page

        headers = {}
        if self._token != "":
            headers["PRIVATE-TOKEN"] = f"{self._token}"

        result = self.combine_sources(payload, headers, page)

        return result

    def combine_sources(self, payload, headers, page):
        scopes = ["projects", "issues", "merge_requests"]
        result = []
        page = Page(page)
        for scope in scopes:
            payload["scope"] = scope
            response = requests.get(
                scope, params=payload, headers=headers).json()
            logger.debug(f"Searching gitlab scope: {scope}")
            if response.status_code == 429:
                self._api_banned_till = datetime.now(
                ) + timedelta(int(response.headers["Retry-After"]))
                logger.warning(
                    f"gitlab search for endpoint {scope} didn't work it as rate limit  was hit")
                continue
            logger.info(
                f"Searching gitlab for {scope} returned {len(response)} results")

            for index, item in enumerate(response):
                link = item['web_url']
                preview = item["description"]
                title = item["path_with_namespace"]

                created_at = datetime.strptime(
                    item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

                single_result = SingleResult(
                    preview, link, SOURCENAME, created_at, CATEGORYY_MAP[scope], title)
                self.__number_of_items += 1
                # first item has higher score
                result.append((single_result, len(response)-index))

        random.shuffle(result)
        result = sorted(result, key=lambda x: x[1])

        logger.info(f"Gitlab returned a total of {len(result)} results")

        if len(result) == 0:
            return

        for item in result:
            page.add(item[0])
        return page

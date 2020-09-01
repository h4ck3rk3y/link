from .search import Search
from ..models.results import Page, SingleResult
import requests
import base64
from datetime import datetime
from datetime import timedelta
from .constants import ISSUE, CODE, REPO
import logging
import random

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

ISSUES_URL = "https://api.github.com/search/issues"
REPO_URL = "https://api.github.com/search/repositories"
CODE_URL = "https://api.github.com/search/code"


attribute_map = {
    "preview": {
        ISSUES_URL: "body",
        REPO_URL: "description",
        CODE_URL: "path"
    },
    "title": {
        ISSUES_URL: "title",
        REPO_URL: "full_name",
        CODE_URL: "name"
    }
}

category_map = {
    ISSUES_URL: ISSUE,
    REPO_URL: REPO,
    CODE_URL: CODE
}

SOURCENAME = "github"

"""
https://docs.github.com/en/rest/reference/search

for authenticated requests github allows 30 queries / minute
for unauthenticated requests github allows 10 queries / minute

to test personal auth you can create a token with repo permissions
and put in your username.
"""

logger = logging.getLogger(__name__)


class Github(Search):

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

        payload = {"q": f"{self._query}"}

        if self._pagesize:
            payload['per_page'] = self._pagesize

        if page:
            payload['page'] = page

        if self._token != "":
            HEADERS["Authorization"] = f"token {self._token}"

        result = self.combine_sources(payload, HEADERS, page)

        return result

    def combine_sources(self, payload, headers, page):
        endpoints = [ISSUES_URL, REPO_URL, CODE_URL]
        if not self._username:
            # code search requires repo, username or org to be set
            del endpoints[2]
        result = []
        page = Page(page)
        for endpoint in endpoints:
            response = requests.get(
                endpoint, params=payload, headers=headers).json()
            logger.debug(f"Searching Github endpoint: {endpoint}")
            if 'items' not in response:
                if response['message'].startswith('API rate limit exceeded'):
                    self._api_banned_till = datetime.now() + timedelta(seconds=60)
                logger.warning(
                    f"github search for endpoint {endpoint} didn't work it failed with. Message: {response['message']}")
                continue
            logger.info(
                f"Searching Github for {endpoint} returned {len(response['items'])} results")
            for item in response['items']:
                link = item['html_url']
                preview = item[attribute_map["preview"][endpoint]]
                title = item[attribute_map["title"][endpoint]]

                # code results don't have created_at
                created_at = None
                if endpoint != CODE_URL:
                    created_at = datetime.strptime(
                        item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

                single_result = SingleResult(
                    preview, link, SOURCENAME, created_at, category_map[endpoint], title)
                self.__number_of_items += 1
                result.append((single_result, item['score']))

        # we randomize the above results and then sort by score
        # this allows different categories of results to appear
        random.shuffle(result)
        result = sorted(result, key=lambda x: x[1])

        logger.info(f"Github returned a total of {len(result)} results")

        if len(result) == 0:
            return

        for item in result:
            page.add(item[0])
        return page

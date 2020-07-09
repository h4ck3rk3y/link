from .search import Search
from ..models.results import Page, SingleResult
import requests
import base64
from datetime import datetime
from .constants import ISSUE
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

URL = "https://api.github.com/search/issues"
SOURCENAME = "github"


class Github(Search):

    def __init__(self, user=None):
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return Github(user)

    def fetch(self, page=0):
        assert(self._query != None and self.query !=
               ""), "Query cannot be empty"

        payload = {"q": f"{self._query}"}

        if self._username:
            payload["q"] = f"{self._query}+user:{self._username}"

        if self._pagesize:
            payload['per_page'] = self._pagesize

        if page:
            payload['page'] = page

        HEADERS["Authorization"] = f"Basic: {self._token}"

        result = Page(page, self._pagesize)
        response = requests.get(URL, params=payload, headers=HEADERS).json()

        if 'items' not in response:
            # for authenticated requests github allows 30 queries / minute
            # for unauthenticated requests github allows 10 queries / minute
            logging.warn(
                f"github search didn't work it failed with. Message: {response['message']}")
            return result

        for item in response['items']:
            link = item['html_url']
            preview = item['body']
            title = item['title']
            created_at = datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            single_result = SingleResult(
                preview, link, SOURCENAME, created_at, ISSUE, title)
            result.add(single_result)

        return result

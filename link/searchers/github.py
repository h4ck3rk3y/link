from .search import Search
from ..models.results import Page, SingleResult
import requests
import base64
from datetime import datetime
from .constants import ISSUE

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

URL = "https://api.github.com/search/issues"
SOURCENAME = "github"


class Github(Search):

    def __init__(self, token=None):
        super().__init__(token=token)

    @staticmethod
    def builder(token=None):
        return Github(token)

    def fetch(self, page=0):
        assert(self._query != None and self.query !=
               ""), "Query cannot be empty"

        # @ToDo add more qualifiers
        # Here we can specify the user and make it personal
        payload = {"q": f"{self._query}"}

        if self._pagesize:
            payload['per_page'] = self._pagesize

        if page:
            payload['page'] = page

        HEADERS["Authorization"] = f"Basic: {self._token}"

        result = Page(page, self._pagesize)
        response = requests.get(URL, params=payload, headers=HEADERS).json()

        # TODO: fix this
        if 'items' not in response:
            print("ERROR!!", response)
            return result

        for item in response['items']:
            link = item['url']
            preview = item['title']
            created_at = datetime.strptime(
                item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            single_result = SingleResult(
                preview, link, SOURCENAME, created_at, ISSUE)
            result.add(single_result)

        return result

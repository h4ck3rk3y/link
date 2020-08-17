from .search import Search
from ..models.results import Page, SingleResult
import requests
from datetime import datetime
from datetime import timedelta
from .constants import MEMBERS, BOARDS, ORGANIZATIONS, CARDS
import logging
import random

from collections import defaultdict

HEADERS = {
    "Accept": "application/json"
}

SEARCH_URL = "https://api.trello.com/1/search/"

SOURCENAME = "trello"

attribute_map = {
    CARDS: {
        "title": "name",
        "preview": "desc",
        "date": "dateLastActivity",
        "link": "shortUrl"
    },
    MEMBERS: {
        "title": "fullName",
        "preview": "username",
        "date": "",
        "link": ""
    },
    BOARDS: {
        "title": "name",
        "preview": "",
        "date": "",
        "link": ""
    },
    ORGANIZATIONS: {
        "title": "displayName",
        "preview": "name",
        "date": "",
        "link": ""
    }
}

"""
Note this needs both token and key. We are using the username field of the UserToken
object to store the key! Buyer beware.

To help prevent strain on Trello’s servers, our API imposes rate limits per API key for all issued tokens.
There is a limit of 300 requests per 10 seconds for each API key and no more than 100 requests per 10 second interval for each token.
If a request exceeds the limit, Trello will return a 429 error.


https://developer.atlassian.com/cloud/trello/rest/api-group-search/#api-search-get
"""

logger = logging.getLogger(__name__)


class Trello(Search):

    def __init__(self, user=None):
        self.__number_of_items = 0
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return Trello(user)

    def fetch(self, page=0):
        assert(self._query != None and self.query !=
               ""), "Query cannot be empty"
        assert(self._token != None and self._token !=
               ""), "Query cannot be empty"
        assert(self._username != None and self._username !=
               ""), "Query cannot be empty"

        status, timelimit = self.rate_limit_exceeded()
        if status:
            logger.warning(
                f"Rate limit has been exceeded, try after {timelimit}")
            return

        if self.__number_of_items >= page*self._pagesize:
            logger.info(
                f"we already seem to have enough results: {self.__number_of_items}, not searching for more")
            return

        payload = {"query": f"{self._query}",
                   "token": self._token, "key": self._username}

        # trello counts from 0
        page = page - 1

        if self._pagesize:
            payload['boards_limit'] = self._pagesize
            payload['cards_limit'] = self._pagesize
            payload['organizations_limit'] = self._pagesize
            payload['members_limit'] = self._pagesize

        if page:
            payload['boards_page'] = page
            payload['cards_page'] = page
            payload['organizations_page'] = page
            payload['members_page'] = page

        logger.debug(f"Searching trello")
        response = requests.get(SEARCH_URL, params=payload)

        if response.status_code == 429:
            self._api_banned_till = datetime.now() + timedelta(secodns=10)
            logger.warning(
                f"API limit reached, please try after {self._api_banned_till}")

        if response.status_code != 200:
            logger.warning(
                "For some reason we couldn't get a succesful response from the API")

        response_as_json = response.json()
        result = self.combine_results(response_as_json, page-1)
        return result

    def combine_results(self, response_as_json, page):
        result = []
        page = Page(page)

        categories = [CARDS, BOARDS, MEMBERS, ORGANIZATIONS]

        for category in categories:
            for index, row in enumerate(response_as_json[category]):

                attributes = attribute_map[category]
                single_result = SingleResult(
                    row.get(attributes["preview"]), row.get(attributes["link"]), SOURCENAME, self.get_date(row.get(attributes["date"])), category, row.get(attributes["title"]))

                score = 100 - index
                self.__number_of_items += 1
                result.append((single_result, score))

        # we randomize the above results and then sort by score
        # this allows different categories of results to appear
        random.shuffle(result)
        result = sorted(result, key=lambda x: x[1])

        logger.info(f"Trello search returned {len(result)} results")

        if len(result) == 0:
            return

        for item in result:
            page.add(item[0])
        return page

    def get_date(self, date_as_str):
        if not date_as_str:
            return None
        return datetime.strptime(
            date_as_str, "%Y-%m-%dT%H:%M:%S.%fZ")

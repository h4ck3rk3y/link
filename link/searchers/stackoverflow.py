from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests
from datetime import datetime
from .constants import QUESTION
import logging

URL = "https://api.stackexchange.com/2.2/search"
SOURCENAME = "stackoverflow"
logger = logging.getLogger(__name__)


class StackOverflow(Search):

    def __init__(self, user=None):
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return StackOverflow(user)

    def fetch(self, page=0):
        assert(self._query != None and self._query !=
               ""), "Query cannot be empty"

        payload = {"intitle": self._query, "site": SOURCENAME}

        if self._enddate:
            payload["todate"] = int(self._enddate.timestamp())
        if self._fromdate:
            payload["fromdate"] = int(self._fromdate.timestamp())
        if self._pagesize:
            payload["pagesize"] = self._pagesize
        if page:
            payload["page"] = page

        response = requests.get(URL, params=payload).json()

        page = Page(page, self._pagesize)

        if 'items' not in response:
            # for searches stack overflow allows about 300 searches
            # without api token per day.
            # with a token that limit is up to 10,000
            logger.warn(
                f"stackoverflow search failed with {response['error_message']}")
            return page

        for item in response['items']:
            preview = self.generate_preview(item)
            title = item['title']
            link = item['link']
            date = datetime.fromtimestamp(item['creation_date'])
            single_result = SingleResult(
                preview, link, SOURCENAME, date, QUESTION, title)
            page.add(single_result)

        return page

    def generate_preview(self, item):
        return f"This question has been viewed {item['view_count']} times and has {item['answer_count']} answers"

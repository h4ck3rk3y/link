from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests
from datetime import datetime
from .constants import QUESTION

URL = "https://api.stackexchange.com/2.2/search"
SOURCENAME = "stackoverflow"


class StackOverflow(Search):

    def __init__(self, token=None):
        super().__init__(token=token)

    @staticmethod
    def builder(token=None):
        return StackOverflow(token)

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

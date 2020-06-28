from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests

URL = "https://api.stackexchange.com/2.2/search"
SOURCENAME = "stackoverflow"
DATE_FORMAT = "YYYY-mm-dd"


class StackOverflow(Search):

    def __init__(self, token=None):
        super().__init__(token=token)

    @staticmethod
    def builder(token=None):
        return StackOverflow(token)

    def fetch(self, page=0):
        assert(self._query != None), "Query cannot be empty"

        payload = {"intitle": self._query, "site": SOURCENAME}

        if self._enddate:
            payload["enddate"] = self._enddate.strftime("DATE_FORMAT")
        if self._fromdate:
            payload["fromdate"] = self._fromdate.srtftime(DATE_FORMAT)
        if self._pagesize:
            payload["pagesize"] = self._pagesize
        if page:
            payload["page"] = page

        response = requests.get(URL, params=payload).json()

        page = Page(page, self._pagesize)

        for item in response['items']:
            preview = item['title']
            link = item['link']
            single_result = SingleResult(preview, link, SOURCENAME)
            page.add(single_result)

        return page

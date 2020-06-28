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

    def fetch(self):
        assert(self._query != None), "Query cannot be empty"

        payload = {"intitle": self._query, "site": SOURCENAME}

        if self._enddate:
            payload["enddate"] = self._enddate.strftime("DATE_FORMAT")
        if self._fromdate:
            payload["fromdate"] = self._fromdate.srtftime(DATE_FORMAT)
        if self._pagesize:
            payload["pagesize"] = self._pagesize
        if self._page:
            payload["page"] = self._page

        response = requests.get(URL, params=payload).json()

        source_result = SourceResult("stackoverflow")
        page = Page(self._page, self._pagesize)

        for item in response['items']:
            preview = item['title']
            link = item['link']
            single_result = SingleResult(preview, link, SOURCENAME)
            page.add(single_result)

        source_result.add(page)

        return source_result

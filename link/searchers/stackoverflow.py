from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests

URL = "https://api.stackexchange.com/2.2/search"
SOURCENAME = "stackoverflow"
DATE_FORMAT = "YYYY-mm-dd"


class StackOverflow(Search):

    def __init__(self):
        super().__init__()

    @staticmethod
    def builder(self, token=None):
        self.__token = token
        return StackOverflow()

    def fetch(self):
        assert(self.__query != None), "Query cannot be empty"

        payload = {"intitle": self.__query}

        if self.__enddate:
            payload["enddate"] = self.__enddate.strftime("DATE_FORMAT")
        if self.__fromdate:
            payload["fromdate"] = self.__fromdate.srtftime(DATE_FORMAT)
        if self.__pagesize:
            payload["pagesize"] = self.__pagesize
        if self.__page:
            payload["page"] = self.__page

        response = requests.get(URL, params=payload).json()

        source_result = SourceResult("stackoverflow")
        page = Page(self.__page, self.__pagesize)

        for item in response['items']:
            preview = item['title']
            link = item['link']
            single_result = SingleResult(preview, link, SOURCENAME)
            page.add(single_result)

        source_result.add(page)

        return source_result

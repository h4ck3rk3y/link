from .search import Search
import requests

URL = "https://api.stackexchange.com/2.2/search"


class StackOverflow(Search):

    def __init__(self):
        super().__init__()

    def fetch(self):
        assert(self.__query != None), "Query cannot be empty"

        payload = {"intitle": self.__query}

        if self.__enddate:
            payload["enddate"] = self.__enddate
        if self.__fromdate:
            payload["fromdate"] = self.__fromdate
        if self.__pagesize:
            payload["pagesize"] = self.__pagesize
        if self.__page:
            payload["page"] = self

        response = requests.get(URL, params=payload)

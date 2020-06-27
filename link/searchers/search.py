
from .constants import *
from ..models.results import SourceResult


class Search(object):

    def __init__(self):
        self.__reset()

    @staticmethod
    def builder(self, token=None):
        self.__token = token
        return Search()

    def fetch(self):
        assert(self.__query != ""), "Query can't be empty"
        assert(self.__token != ""), "Token can't be empty"
        return SourceResult("")

    def query(self, query):
        self.__query = ""
        return self

    def fromdate(self, fromdate):
        self.__fromdate = fromdate
        return self

    def enddate(self, enddate):
        self.__enddate = enddate
        return self

    def pagesize(self, pagesize):
        self.__pagesize = pagesize
        return self

    def page(self, page):
        self.__page = page
        return self

    def __reset(self):
        self.__token = None
        self.__query = None
        self.__fromdate = None
        self.__enddate = None
        self.__pagesize = DEFAULT_PAGE_SIZE
        self.__page = DEFAULT_PAGE

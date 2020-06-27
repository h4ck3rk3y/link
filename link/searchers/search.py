
from .constants import *
from ..models.results import SourceResult
from ..decorators import immutable


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

    @immutable("query")
    def query(self, query):
        self.__query = query
        return self

    @immutable("fromdate")
    def fromdate(self, fromdate):
        self.__fromdate = fromdate
        return self

    @immutable("enddate")
    def enddate(self, enddate):
        self.__enddate = enddate
        return self

    @immutable("pagesize", DEFAULT_PAGE_SIZE)
    def pagesize(self, pagesize):
        self.__pagesize = pagesize
        return self

    @immutable("page", DEFAULT_PAGE)
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

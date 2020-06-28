
from .constants import *
from ..models.results import SourceResult
from ..decorators import immutable


class Search(object):

    def __init__(self, token):
        self.__token = token
        self.__reset()

    @staticmethod
    def builder(token=None):
        return Search(token)

    def fetch(self):
        assert(self.__query != ""), "Query can't be empty"
        assert(self.__token != ""), "Token can't be empty"
        return SourceResult("")

    @immutable("query")
    def query(self, query):
        self._query = query
        return self

    @immutable("fromdate")
    def fromdate(self, fromdate):
        self._fromdate = fromdate
        return self

    @immutable("enddate")
    def enddate(self, enddate):
        self._enddate = enddate
        return self

    @immutable("pagesize", DEFAULT_PAGE_SIZE)
    def pagesize(self, pagesize):
        self._pagesize = pagesize
        return self

    @immutable("page", DEFAULT_PAGE)
    def page(self, page):
        self._page = page
        return self

    def __reset(self):
        self._query = None
        self._fromdate = None
        self._enddate = None
        self._pagesize = DEFAULT_PAGE_SIZE
        self._page = DEFAULT_PAGE

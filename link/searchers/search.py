
from .constants import DEFAULT_PAGE_SIZE
from ..models.results import Page
from ..decorators import immutable
from datetime import datetime


class Search(object):

    def __init__(self, user):
        self._username = user.username
        self._token = user.token
        self._api_banned_till = None
        self.__reset()

    @staticmethod
    def builder(token=None):
        return Search(token)

    def fetch(self, page=0):
        assert(self._query != ""), "Query can't be empty"
        assert(self._token != ""), "Token can't be empty"
        return Page(0)

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

    def rate_limit_exceeded(self):
        if self._api_banned_till is None:
            return False, None
        current_date = datetime.now()
        if current_date < self._api_banned_till:
            return True, self._api_banned_till
        else:
            self._api_banned_till = None
            return False, None

    def __reset(self):
        self._query = None
        self._fromdate = None
        self._enddate = None
        self._pagesize = DEFAULT_PAGE_SIZE

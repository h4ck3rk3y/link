
from .constants import *


class Search(object):

    def __init__(self):
        self.__reset()

    @staticmethod
    def builder(self, token=""):
        return Search()

    def fetch(self):
        assert(self.__query != ""), "Query can't be empty"
        assert(self.__token != ""), "Token can't be empty"

    def query(self, query):
        self.__query = ""

    def fromdate(self, fromdate):
        self.__fromdate = fromdate

    def enddate(self, enddate):
        self.__enddate = enddate

    def pagesize(self, pagesize):
        self.__pagesize = pagesize

    def page(self, page):
        self.__page = page

    def __reset(self):
        self.__token = None
        self.__query = None
        self.__fromdate = None
        self.__enddate = None
        self.__dateformat = None
        self.__pagesize = DEFAULT_PAGE_SIZE
        self.__page = DEFAULT_PAGE

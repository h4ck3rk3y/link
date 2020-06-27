from .user import UserTokens

DEFAULT_PAGE_SIZE = 15


class SourcesEnabled(object):

    def __init__(self, slack=True, github=True, stackoverflow=True, trello=True):
        self.__slack = slack
        self.__github = github
        self.__trello = trello
        self.__stackoverflow = stackoverflow


class Statistics(object):
    def __init__(self, slack=0, github=0, stackoverflow=0, trello=0):
        self.__slack = slack
        self.__github = github
        self.__trello = trello
        self.__stackoverflow = stackoverflow

    """you should be able to access statistics.slack etc"""


class SingleResult(object):
    def __init__(self):
        self.preview = "preview Text"
        self.source = "name of the source"
        self.link = "link"


class Results(object):
    """ Any of the search query will return a Results object

    To find out the total number of results use
    results.hits

    To get a list of result objects use
    results.results

    To get the current page number use
    results.page_number

    To get the total number(without paging) of slack results
    results.statistics.slack

    """

    def __init__(self, statistics=None):
        # a statistics object
        self.__statistics = statistics
        # number of results in current result object
        self.__hits = 7
        # size of the page
        self.__page_size = DEFAULT_PAGE_SIZE
        # a list of result objects as big as the page size
        self.__results = [SingleResult]
        # current page number
        self.__page_number = 0

    @property
    def statistics(self):
        return self.__statistics


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user: UserTokens):

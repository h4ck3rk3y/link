from .models.user_tokens import UserTokens
from .models.sources_enabled import SourcesEnabled
from .searchers.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from .searchers.stackoverflow import StackOverflow
from .models.results import Results
from .decorators import immutable


###
# @ToDo will probably tweak this a little to not support page number but
# instead support a next() button
# The backend could create a search using the builder call fetch
# return results to the user, persist the object somewhere, redis?, dictionary?
# if the user requests another page then the backend can call next()
###
class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        """ sources enabled being set to None implies all integrations for which token is set will be searched"""
        self.__sources_enabled = sources_enabled
        self.__user_tokens = user_tokens
        super().__init__()
        self.__reset()

    @staticmethod
    def builder(self):
        return Link(self.__user_tokens, self.__sources_enabled)

    def fetch(self):
        self.__validate()
        result = Results()

        if self.__sources_enabled.stackoverflow:
            stackoverflow = StackOverflow.builder(UserTokens.stackoverflow).fromdate(self.__fromdate).enddate(
                self.__enddate).query(self.__query).page(self.__page).pagesize(self.__page_size).fetch()
            result.add_source(stackoverflow)

        return result

    @immutable("page_size", DEFAULT_PAGE_SIZE)
    def page_size(self, page_size):
        self.__page_size = page_size
        return self

    @immutable("page", DEFAULT_PAGE)
    def page(self, page):
        self.__page_size = page
        return self

    @immutable("formdate")
    def fromdate(self, fromdate):
        self.__fromdate = fromdate
        return self

    @immutable("enddate")
    def enddate(self, enddate):
        self.__enddate = enddate
        return self

    @immutable("query")
    def query(self, query):
        self.__query = query
        return self

    def slack_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.slack = True
        return self

    def not_slack(self):
        self.__sources_enabled.slack = False
        return self

    def github_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.github = True
        return self

    def not_github(self):
        self.__sources_enabled.github = False
        return self

    def trello_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.trello = True
        return self

    def not_trello(self):
        self.__sources_enabled.trello = False
        return self

    def stackoverflow_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.stackoverflow = True
        return self

    def not_stackoverflow(self):
        self.__sources_enabled.stackoverflow = False
        return self

    def __disable_all_sources(self):
        self.__sources_enabled.slack = False
        self.__sources_enabled.stackoverflow = False
        self.__sources_enabled.trello = False
        self.__sources_enabled.github = False

    def __validate(self):
        assert(self.__query != None), "Query cant be None"
        assert(self.__query != ""), "Query cant be empty"
        assert(self.__user_tokens != None), "User Tokens cant be none"
        assert(self.__sources_enabled.slack or self.__sources_enabled.stackoverflow or self.__sources_enabled.github or self.__sources_enabled.trello != False), "No source enabled"
        assert(self.__built != False), "Build hasn't been called"

    def __reset(self):
        self.__page = DEFAULT_PAGE
        self.__page_size = DEFAULT_PAGE_SIZE
        self.__fromdate = None
        self.__enddate = None
        self.__query = None
        self.__built = False

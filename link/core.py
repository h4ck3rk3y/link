from .models.user_tokens import UserTokens
from .models.sources_enabled import SourcesEnabled
from .searchers.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        """ sources enabled being set to None implies all integrations for which token is set will be searched"""
        self.__sources_enabled = sources_enabled
        self.__user_tokens = user_tokens
        super().__init__()

    def slack_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.slack = True

    def not_slack(self):
        self.__sources_enabled.slack = False

    def github_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.github = True

    def not_github(self):
        self.__sources_enabled.github = False

    def trello_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.trello = True

    def not_trello(self):
        self.__sources_enabled.trello = False

    def stackoverflow_only(self):
        self.__disable_all_sources()
        self.__sources_enabled.stackoverflow = True

    def not_stackoverflow(self):
        self.__sources_enabled.stackoverflow = False

    def __disable_all_sources(self):
        self.__sources_enabled.slack = False
        self.__sources_enabled.stackoverflow = False
        self.__sources_enabled.trello = False
        self.__sources_enabled.github = False

    def __reset__(self):
        self.__page = DEFAULT_PAGE
        self.__page_size = DEFAULT_PAGE_SIZE
        self.fromdate = None
        self.enddate = None
        self.query = None

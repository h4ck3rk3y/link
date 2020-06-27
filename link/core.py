from .user import UserTokens

DEFAULT_PAGE_SIZE = 15


class SourcesEnabled(object):

    def __init__(self, slack=True, github=True, stackoverflow=True, trello=True):
        self.__slack = slack
        self.__github = github
        self.__trello = trello
        self.__stackoverflow = stackoverflow


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user: UserTokens, sources: SourcesEnabled):

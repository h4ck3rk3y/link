from .models.user_tokens import UserTokens
from .models.sources_enabled import SourcesEnabled
from .searchers.constants import DEFAULT_PAGE_SIZE
from .searchers.stackoverflow import StackOverflow
from .searchers.github import Github
from .searchers.slack import Slack
from .searchers.trello import Trello
from .models.results import Results, SourceResult
from .decorators import immutable


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        """ sources enabled being set to None implies all integrations for which token is set will be searched"""
        self.__sources_enabled = sources_enabled
        self.__user_tokens = user_tokens
        if self.__sources_enabled is None:
            stackoverflow = user_tokens.stackoverflow is not None
            trello = user_tokens.trello is not None
            github = user_tokens.github is not None
            slack = user_tokens.slack is not None
            self.__sources_enabled = SourcesEnabled(
                stackoverflow=stackoverflow, github=github, trello=trello, slack=slack)

        super().__init__()
        self.__page = 1
        self.__pages = []
        self.__results = Results()

        if self.__sources_enabled.stackoverflow:
            self.__stackoverflow = None
            self.__stackoverflow_result = SourceResult("stackoverflow")

        if self.__sources_enabled.github:
            self.__github = None
            self.__github_result = SourceResult("github")

        if self.__sources_enabled.slack:
            self.__slack = None
            self.__slack_result = SourceResult("slack")

        if self.__sources_enabled.trello:
            self.__trello = None
            self.__trello_result = SourceResult("trello")

        self.__reset()

    @staticmethod
    def builder(user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        return Link(user_tokens, sources_enabled)

    def fetch(self):
        self.__validate()

        if len(self.__pages) >= self.__page:
            self.__page += 1
            return self.__pages[self.__page-2]

        if self.__results.unfetched_results() >= self.__page_size:
            self.__page += 1
            output = self.__results.topk(self.__page_size)
            self.__pages.append(output)
            return output

        if self.__sources_enabled.stackoverflow:
            if not self.__stackoverflow:
                self.__stackoverflow = StackOverflow.builder(self.__user_tokens.stackoverflow).fromdate(self.__fromdate).enddate(
                    self.__enddate).query(self.__query).pagesize(self.__page_size)

            page = self.__stackoverflow.fetch(self.__page)
            self.__stackoverflow_result.add(page)
            self.__results.add_source_result(self.__stackoverflow_result)

        if self.__sources_enabled.github:
            if not self.__github:
                self.__github = Github.builder(
                    self.__user_tokens.github).query(self.__query).pagesize(self.__page_size)
            page = self.__github.fetch(self.__page)
            self.__github_result.add(page)
            self.__results.add_source_result(self.__github_result)

        if self.__sources_enabled.slack:
            if not self.__slack:
                self.__slack = Slack.builder(self.__user_tokens.slack).query(
                    self.__query).pagesize(self.__page_size)
            page = self.__slack.fetch(self.__page)
            self.__slack_result.add(page)
            self.__results.add_source_result(self.__slack_result)

        if self.__sources_enabled.trello:
            if not self.__trello:
                self.__trello = Trello.builder(self.__user_tokens.trello).query(
                    self.__query).pagesize(self.__page_size)
            page = self.__trello.fetch(self.__page)
            self.__trello_result.add(page)
            self.__results.add_source_result(self.__trello_result)

        self.__page += 1
        output = self.__results.topk(self.__page_size)
        self.__pages.append(output)
        return output

    def previous(self):
        if self.__page < 3:
            return []
        self.__page -= 1
        return self.__pages[self.__page-2]

    def stackoverflow_rate_limit_exceeded(self):
        if self.__stackoverflow:
            return self.__stackoverflow.rate_limit_exceeded()

    def github_rate_limit_exceeded(self):
        if self.__github:
            return self.__github.rate_limit_exceeded()

    def slack_rate_limit_exceeded(self):
        if self.__slack:
            return self.__slack.rate_limit_exceeded()

    def trello_rate_limit_exceeded(self):
        if self.__trello:
            return self.__slack.rate_limit_exceeded()

    @immutable("page_size", DEFAULT_PAGE_SIZE)
    def page_size(self, page_size):
        self.__page_size = page_size
        return self

    @immutable("fromdate")
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

    def __reset(self):
        self.__page_size = DEFAULT_PAGE_SIZE
        self.__fromdate = None
        self.__enddate = None
        self.__query = None

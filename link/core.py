from .models.user_tokens import UserTokens
from .models.sources_enabled import SourcesEnabled
import os
from .searchers.constants import DEFAULT_PAGE_SIZE, GITHUB_QUALIFIERS
from importlib import import_module
from .models.results import Results, SourceResult
from .decorators import immutable
import logging
import re
from collections import defaultdict

logger = logging.getLogger(__name__)


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        """ sources enabled being set to None implies all integrations for which token is set will be searched"""
        self.__sources_enabled = sources_enabled
        self.__user_tokens = user_tokens
        if self.__sources_enabled is None:
            self.__sources_enabled = self.__user_tokens.tokens.keys()

        super().__init__()
        self.__page = 1
        self.__pages = []
        self.__results = Results()
        self.__source_results = {}
        self.__fetchers_modules = {}
        self.__fetchers = defaultdict(list)

        for source in self.__sources_enabled:
            self.__source_results[source] = SourceResult("source")

        self.load_searchers()
        self.__reset()

    @staticmethod
    def builder(user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        return Link(user_tokens, sources_enabled)

    def fetch(self):
        self.__validate()

        if len(self.__pages) >= self.__page:
            logger.info(
                "We don't have to load another page as its already been loaded")
            self.__page += 1
            return self.__pages[self.__page-2]

        if self.__results.unfetched_results() >= self.__page_size:
            self.__page += 1
            output = self.__results.topk(self.__page_size)
            self.__pages.append(output)
            return output

        # page = self.__stackoverflow.fetch(self.__page)
        # self.__stackoverflow_result.add(page)
        # self.__results.add_source_result(self.__stackoverflow_result)

        if self.__fetchers:
            for source in self.__sources_enabled.tokens:
                for _, module in self.__fetchers_modules:
                    if module.source == source:
                        self.__fetchers[source].append(
                            module(self.__user_tokens[source].token, self.__user_tokens[source].username, self.__query, self.__page_size))

        self.__page += 1
        output = self.__results.topk(self.__page_size)
        self.__pages.append(output)
        return output

    def load_searchers(self):
        fetchers = {}
        for searcher in os.listdir("./searchers"):
            if searcher.startswith("link_"):
                searcher_name = searcher.replace(".py", "")
                fetchers[searcher_name] = import_module(
                    f"searchers.{searcher_name}")
        self.__fetchers_modules = fetchers

    @staticmethod
    def remove_github_filters(query):
        regex_exp_for_qualifiers = r'([\w-]+:[\w-]+)'

        for potential_qualifier in re.findall(regex_exp_for_qualifiers, query):
            if potential_qualifier in GITHUB_QUALIFIERS or potential_qualifier.split(':')[0] in GITHUB_QUALIFIERS:
                query = query.replace(potential_qualifier, "")

        return re.sub(r'\s+', ' ', query).strip()

    def previous(self):
        if self.__page < 3:
            logger.info("Went too far back, this page doesn't exist")
            return []
        logger.info("Fetching a previous page")
        self.__page -= 1
        return self.__pages[self.__page-2]

    @immutable("page_size", DEFAULT_PAGE_SIZE)
    def page_size(self, page_size):
        self.__page_size = page_size
        return self

    @immutable("query")
    def query(self, query):
        self.__query = query
        self.__non_github_query = Link.remove_github_filters(query)
        logger.debug(
            f"Filtered query is  raw query: {self.__non_github_query == self.__query}")
        return self

    def __disable_all_sources(self):
        self.__sources_enabled = []

    def __validate(self):
        assert(self.__query != None), "Query cant be None"
        assert(self.__query != ""), "Query cant be empty"
        assert(self.__user_tokens != None), "User Tokens cant be none"
        assert(len(self.__sources_enabled) > 0), "No source enabled"

    def __reset(self):
        self.__page_size = DEFAULT_PAGE_SIZE
        self.__query = None

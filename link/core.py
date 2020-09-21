from .models.user_tokens import UserTokens
from .models.sources_enabled import SourcesEnabled
import os
from .searchers.constants import DEFAULT_PAGE_SIZE
from importlib import import_module
from .models.results import Results, SourceResult
from .decorators import immutable
import logging
import re
from collections import defaultdict
from pathlib import Path
import grequests

logger = logging.getLogger(__name__)


class Link(object):
    """ this is the core class and should be used outside
    the package for search """

    def __init__(self, user_tokens: UserTokens, sources_enabled: SourcesEnabled = None):
        """ sources enabled being set to None implies all integrations for which token is set will be searched"""
        self.__sources_enabled = sources_enabled
        self.__user_tokens = user_tokens
        if self.__sources_enabled is None:
            self.__sources_enabled = SourcesEnabled(
                self.__user_tokens.tokens.keys())

        super().__init__()
        self.__page = 1
        self.__pages = []
        self.__results = Results()
        self.__source_results = {}
        self.__fetchers_modules = {}
        self.__fetchers = defaultdict(list)
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

        if not self.__fetchers:
            self.initialize_fetchers()

        requests = []
        for source in self.__sources_enabled.tokens:
            for fetcher in self.__fetchers[source]:
                request = fetcher.construct_request(self.__page)
                if request is not None:
                    requests.append(request)

        grequests.map(requests)

        self.__page += 1
        output = self.__results.topk(self.__page_size)
        self.__pages.append(output)
        return output

    def load_searchers(self):
        fetchers = {}
        searcher_directory = Path(__file__).parent / "searchers"
        for searcher in os.listdir(searcher_directory):
            if searcher.startswith("link_"):
                searcher_name = searcher.replace(".py", "")
                fetchers[searcher_name] = import_module(
                    f".searchers.{searcher_name}", package="link")
        self.__fetchers_modules = fetchers

    def initialize_fetchers(self):
        for source in self.__sources_enabled.tokens:
            source_result = SourceResult(source)
            for name, module in self.__fetchers_modules.items():
                if module.Searcher.source == source:
                    logger.debug(
                        f"Creating fetcher for {source} with module {name}")
                    self.__source_results[module.Searcher.source] = source_result
                    self.__results.add_source_result(source_result)
                    self.__fetchers[source].append(
                        module.Searcher(self.__user_tokens.tokens[source].token, self.__user_tokens.tokens[source].username, self.__query, self.__page_size, source_result))

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
        return self

    def __disable_all_sources(self):
        self.__sources_enabled = []

    def __validate(self):
        assert(self.__query != None), "Query cant be None"
        assert(self.__query != ""), "Query cant be empty"
        assert(self.__user_tokens != None), "User Tokens cant be none"
        assert(len(self.__sources_enabled.tokens) > 0), "No source enabled"
        assert(set(self.__sources_enabled.tokens).issubset(
            self.__user_tokens.tokens.keys())), "More sources enabled than tokens provided"

    def __reset(self):
        self.__page_size = DEFAULT_PAGE_SIZE
        self.__query = None

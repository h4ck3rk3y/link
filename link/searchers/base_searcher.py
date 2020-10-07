from ..models.results import Page
from datetime import datetime
import grequests
from typing import Tuple
import logging
import re

logger = logging.getLogger(__name__)


class BaseSearcher(object):

    def __init__(self, token, username, query, per_page, source_result, name, user_only, acceptable_qualifiers=set()):
        self.token = token
        self.username = username
        self.query = query
        self.per_page = per_page
        self.rate_limit_expiry = None
        self.name = name
        self.source_result = source_result
        self.errored = False
        self.exhausted = False
        self.acceptable_qualifiers = acceptable_qualifiers
        self.user_only = user_only

        self.remove_non_acceptable_qualifiers()
        assert(type(query) == str and query !=
               ""), "Query has to be a non empty string"

    def construct_request(self, page=0) -> grequests.AsyncRequest:
        """ creates a request from query, token and other parameters.
        """
        if self.rate_limit_exceeded():
            logger.warning(
                f"Skipping {self.name} as rate limit is exceeded")
            return None
        elif self.irrecoverable_error():
            logger.warning(
                f"Skipping {self.name} as last run ran into an unknown error")
            return None
        elif self.is_exhausted():
            logger.info(
                f"Skipping {self.name} as all results have been retrieved")
            return None

        url, payload, headers = self.construct_request_parts(page)
        return grequests.get(url, params=payload, headers=headers, hooks={"response": [self.validate_and_parse]})

    def construct_request_parts(self, page) -> Tuple[str, dict, dict]:
        """ returns url, payload, headers """
        raise NotImplementedError("define the method in the derived class")

    def parse(self, response) -> Page:
        """ parses the response and returns a page object"""
        raise NotImplementedError("define the method in the dervied class")

    def validate(self, response) -> Tuple[bool, datetime]:
        """ validate the response to check if its indeed expected otherwise raise
        errors. Also validate if rate limits have been violated"""
        raise NotImplementedError("define the method in the derived class")

    def validate_and_parse(self, response, **kwargs) -> None:
        status, banned_till = self.validate(response)
        if not status:
            logger.warning(
                f"Response isn't valid for {self.name} not proceeding")
            if banned_till:
                logger.warning(
                    f"Rate limit exceeded for {self.name}, try after {banned_till}")
                self.rate_limit_expiry = banned_till
            else:
                self.errored = True
            return None
        page = self.parse(response.json())
        if len(page) != self.per_page:
            self.exhausted = True
        logger.info(f"Received {len(page)} results from {self.name}")
        if self.user_only:
            for result in page:
                result.user = True
        self.source_result.add(page)
        return None

    def rate_limit_exceeded(self) -> bool:
        """ parses a response and checks whether rate limits have been violated """
        if self.rate_limit_expiry and self.rate_limit_expiry > datetime.now():
            return True
        return False

    def irrecoverable_error(self) -> bool:
        return self.errored

    def is_exhausted(self) -> bool:
        return self.exhausted

    def remove_non_acceptable_qualifiers(self):
        query = self.query
        regex_exp_for_qualifiers = r'([\w-]+:[\w-]+)'
        for potential_qualifier in re.findall(regex_exp_for_qualifiers, query):
            if not(potential_qualifier in self.acceptable_qualifiers or potential_qualifier.split(':')[0] in self.acceptable_qualifiers):
                query = query.replace(potential_qualifier, "")

        self.query = re.sub(r'\s+', ' ', query).strip()

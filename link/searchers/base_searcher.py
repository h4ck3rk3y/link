from ..models.results import Page
from datetime import datetime
from grequests import AsyncRequest
from typing import Tuple
import logging
logger = logging.getLogger(__name__)


class BaseSearcher(object):

    def __init__(self, token, username, query, per_page, source_result, name):
        self.token = token
        self.username = username
        self.query = query
        self.per_page = per_page
        self.rate_limit_expiry = None
        self.name = name
        self.source_result = source_result
        assert(type(query) == str and query !=
               ""), "Query has to be a non empty string"

    def construct_request(self, page=0, user_only=False) -> AsyncRequest:
        """ creates a request from query, token and other parameters.
        """
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
            logger.warn(
                f"Response isn't valid for {self.name} not proceeding")
            if banned_till:
                logger.warn(f"Rate limit exceeded for {self.name}")
                self.rate_limit_expiry = banned_till
            return None
        self.source_result.add(self.parse(response))
        return None

    def rate_limit_exceeded(self):
        """ parses a response and checks whether rate limits have been violated """
        if self.rate_limit_expiry and self.rate_limit_expiry > datetime.now():
            return True

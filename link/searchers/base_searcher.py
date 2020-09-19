from ..models.results import Page
from datetime import datetime
from grequests import AsyncRequest
from typing import Tuple
import logging
logger = logging.getLogger(__name__)


class BaseSearcher(object):

    def __init__(self, token, username, query, per_page, sourcename):
        self.token = token
        self.username = username
        self.query = query
        self.per_page = per_page
        self.rate_limit_expiry = None
        self.sourcename = sourcename

        assert(type(query) == str and query !=
               ""), "Query has to be a non empty string"

    def construct_request(self, page=0, user_only=False) -> AsyncRequest:
        """ creates a request from query, token and other parameters.
        """
        raise NotImplementedError("define the method in the derived class")

    def parse(self, response, page) -> Page:
        """ parses the response and sends returns a page"""
        raise NotImplementedError("define the method in the dervied class")

    def validate(self, response) -> Tuple[bool, datetime]:
        """ validate the response to check if its indeed expected otherwise raise
        errors. Also validate if rate limits have been violated"""
        raise NotImplementedError("define the method in the derived class")

    def validate_and_parse(self, response, page=0) -> Page:
        status, banned_till = self.validate(response)
        if not status:
            logger.warn("Response isn't valid not proceeding")
            if banned_till:
                logger.warn("Rate limit exceeded")
                self.rate_limit_expiry = banned_till
            return None
        return self.parse(response, page)

    def rate_limit_exceeded(self):
        """ parses a response and checks whether rate limits have been violated """
        if self.rate_limit_expiry > datetime.now():
            return True

from ..models.results import Page
from datetime import datetime
from grequests import AsyncRequest
import logging
logger = logging.getLogger(__name__)


class BaseSearcher(object):

    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.rate_limit_expiry = None

    def construct_request(self, page=0, user_only=False) -> AsyncRequest:
        """ creates a request from query, token and other parameters.
        """
        raise NotImplementedError("define the method in the derived class")

    def parse(self, response) -> Page:
        """ parses the response and sends returns a page"""
        raise NotImplementedError("define the method in the dervied class")

    def validate(self, response) -> bool:
        """ validate the response to check if its indeed expected otherwise raise
        errors. Also validate if rate limits have been violated"""
        raise NotImplementedError("define the method in the derived class")

    def validate_and_parse(self, response) -> Page:
        if not self.validate(response):
            logger.warn("Response isn't valid not proceeding")
            return None
        return self.parse(response)

    def rate_limit_exceeded(self):
        """ parses a response and checks whether rate limits have been violated """
        if self.rate_limit_expiry > datetime.now():
            return True

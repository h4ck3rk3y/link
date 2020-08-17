from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests
from datetime import datetime
from .constants import MESSAGE
import logging
from datetime import timedelta
import re

URL = "https://slack.com/api/search.messages"
SOURCENAME = "slack"

"""
just exploring the slack api here
Documentation: https://api.slack.com/methods/search.messages
At the time of writing slack api didn't support filteirng by date.

Slack allows atleast 20 requests per minute
Search is tier 2
https://api.slack.com/docs/rate-limits#tier_t2
"""

HEADERS = {"Content-type": "application/x-www-form-urlencoded"}


class Slack(Search):

    def __init__(self, user=None):
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return Slack(user)

    def fetch(self, page=0):
        assert(self._query != None and self._query !=
               ""), "Query cannot be empty"

        assert(self._token != None and self._token !=
               ""), "Token cannot be empty"

        payload = {"query": self._query, "token": self._token}

        status, timelimit = self.rate_limit_exceeded()
        if status:
            logging.warning(
                f"Rate limit has been exceeded, try after {timelimit}")
            return

        if self._pagesize:
            payload["count"] = self._pagesize
        if page:
            payload["page"] = page

        logging.debug("Searching Slack")
        response = requests.get(URL, params=payload, headers=HEADERS)

        response_json = response.json()

        page = Page(page)

        if not response_json['ok']:
            logging.warning(
                f"slack search failed with {response_json['error']}")
            if response.status_code == 429:
                retry_after = int(response.headers["Retry-After"])
                logger.warning(
                    f"Rate limit exceeded, we should retry after {retry_after} seconds")
                self._api_banned_till = datetime.now() + timedelta(seconds=retry_after)
            return

        if "messages" not in response_json or "matches" not in response_json["messages"]:
            logging.warning("Status okay but no matches")
            return

        logging.info(
            f"Slack returned {len(response['messages']['matches'])} results")

        for message in response_json["messages"]["matches"]:
            preview = message["text"]
            title = f"Message from {message['username']} on #{message['channel']['name']}"
            link = message['permalink']
            date = datetime.fromtimestamp(float(message['ts']))
            single_result = SingleResult(
                preview, link, SOURCENAME, date, MESSAGE, title)
            page.add(single_result)

        return page

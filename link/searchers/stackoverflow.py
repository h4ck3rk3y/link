from .search import Search
from ..models.results import SingleResult, SourceResult, Page
import requests
from datetime import datetime
from .constants import QUESTION
import logging
from datetime import timedelta
import re

URL = "https://api.stackexchange.com/2.2/search"
SOURCENAME = "stackoverflow"

"""
for searches stack overflow allows about 300 searches
without api token per day.
with a token that limit is up to 10,000

in so the searches can't be personalized

"""


class StackOverflow(Search):

    def __init__(self, user=None):
        super().__init__(user=user)

    @staticmethod
    def builder(user=None):
        return StackOverflow(user)

    def fetch(self, page=0):
        assert(self._query != None and self._query !=
               ""), "Query cannot be empty"

        payload = {"intitle": self._query, "site": SOURCENAME}

        status, timelimit = self.rate_limit_exceeded()
        if status:
            logging.warning(
                f"Rate limit has been exceeded, try after {timelimit}")
            return

        if self._enddate:
            payload["todate"] = int(self._enddate.timestamp())
        if self._fromdate:
            payload["fromdate"] = int(self._fromdate.timestamp())
        if self._pagesize:
            payload["pagesize"] = self._pagesize
        if page:
            payload["page"] = page

        logging.info("Searching Stackoverflow")
        response = requests.get(URL, params=payload).json()

        page = Page(page)

        if 'items' not in response:
            logging.warning(
                f"stackoverflow search failed with {response['error_message']}")
            if response['error_message'].startswith('too many requests from this IP'):
                banned_until = self.parse_time_from_message(
                    response['error_message'])
                self._api_banned_till = datetime.now() + timedelta(seconds=banned_until)
            return

        logging.info(f"Stacksearch returned {len(response['items'])} results")

        for item in response['items']:
            preview = self.generate_preview(item)
            title = item['title']
            link = item['link']
            date = datetime.fromtimestamp(item['creation_date'])
            single_result = SingleResult(
                preview, link, SOURCENAME, date, QUESTION, title)
            page.add(single_result)

        return page

    def generate_preview(self, item):
        return f"This question has been viewed {item['view_count']} times and has {item['answer_count']} answers"

    def parse_time_from_message(self, message):
        pattern = re.compile("\\d+")
        result = pattern.search(message)
        return int(result.group(0))

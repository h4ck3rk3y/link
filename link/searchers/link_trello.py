from .base_searcher import BaseSearcher
from ..models.results import SingleResult, SourceResult, Page
from datetime import datetime
from .constants import CARDS, TRELLO_GITLAB_TIME_FORMAT
from datetime import timedelta

"""
Note this needs both token and key. We are using the username field of the UserToken
object to store the key! Buyer beware.

To help prevent strain on Trello’s servers, our API imposes rate limits per API key for all issued tokens.
There is a limit of 300 requests per 10 seconds for each API key and no more than 100 requests per 10 second interval for each token.
If a request exceeds the limit, Trello will return a 429 error.


https://developer.atlassian.com/cloud/trello/rest/api-group-search/#api-search-get
"""


class TrelloSearcher(BaseSearcher):

    source = "trello"
    url = "https://api.trello.com/1/search/"
    name = "trello"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        self.key = user_token.extra_data["key"]
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        payload = {"token": self.token,
                   "key": self.key, "query": self.query, "cards_page": page - 1, "cards_limit": self.per_page, "modelTypes": CARDS}
        return self.url, payload, None

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_until = datetime.now() + timedelta(seconds=10)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        result_page = Page()
        for item in response[CARDS]:
            single_result = SingleResult(
                preview=item["desc"],
                title=item["name"],
                link=item["shortUrl"],
                date=self.get_date(item["dateLastActivity"]),
                source=self.source,
                category=CARDS
            )
            result_page.add(single_result)
        return result_page

    @staticmethod
    def get_date(date_as_str):
        if not date_as_str:
            return None
        return datetime.strptime(
            date_as_str, TRELLO_GITLAB_TIME_FORMAT)

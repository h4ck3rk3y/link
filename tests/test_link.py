from link.core import Link
from link.models.user_tokens import UserTokens, UserToken
import unittest
from datetime import datetime


class TestLink(unittest.TestCase):

    def test_query_cleanup_for_pure_string_match(self):

        query = "foobar is:public going"
        result = "foobar going"

        user_token = UserTokens(
            stackoverflow=UserToken(token=""))
        link = Link.builder(user_token).query(query)

        self.assertEqual(link.remove_github_filters(query), result)

    def test_query_for_regex_match(self):

        query = "foobar is:public user:h4ck3rk3y can be user:psdh org:darkstark going"
        result = "foobar can be going"

        user_token = UserTokens(
            stackoverflow=UserToken(token=""))
        link = Link.builder(user_token).query(query)

        self.assertEqual(link.remove_github_filters(query), result)

    def test_query_that_ends_in_direct_match(self):
        query = "memes is:private"
        result = "memes"

        user_token = UserTokens(
            stackoverflow=UserToken(token=""))
        link = Link.builder(user_token).query(query)

        self.assertEqual(link.remove_github_filters(query), result)

    def test_query_that_ends_in_regex_match(self):
        query = "memes user:psdh"
        result = "memes"

        user_token = UserTokens(
            stackoverflow=UserToken(token=""))
        link = Link.builder(user_token).query(query)

        self.assertEqual(link.remove_github_filters(query), result)

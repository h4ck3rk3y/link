from link.core import Link
from link.models.user_tokens import UserTokens
import unittest


class TestLink(unittest.TestCase):

    def test_links_build(self):
        user_token = UserTokens(stackoverflow=True)
        link = Link.builder(user_token).query("foo").fetch()
        self.assertIsNotNone(link, "link shouldnt be none")

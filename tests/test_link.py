from link.core import Link
from link.models.user_tokens import UserTokens
import unittest
from datetime import datetime


class TestLink(unittest.TestCase):

    def test_links_build(self):
        user_token = UserTokens(
            stackoverflow="not really needed for stackoverflow to work")
        link = Link.builder(user_token).query("foo").page_size(5)
        first_set = set([x.preview for x in link.fetch()])
        second_set = set([x.preview for x in link.fetch()])
        third_set = set([x.preview for x in link.fetch()])
        self.assertIsNotNone(link, "link shouldnt be none")
        self.assertLessEqual(len(second_set), len(first_set))
        self.assertLessEqual(len(third_set), len(second_set))
        self.assertNotEqual(first_set, second_set)
        self.assertNotEqual(third_set, second_set)

    def test_date_filtering_works(self):
        user_token = UserTokens(
            stackoverflow="not really needed for stackoverflow to work")
        link = Link.builder(user_token).query(
            "python").page_size(15).fromdate(datetime(2015, 5, 23)).enddate(datetime(2015, 5, 31))

        results = link.fetch()

        for result in results:
            date = result.date
            self.assertEqual(date.year, 2015)
            self.assertEqual(date.month, 5)
            self.assertGreaterEqual(date.day, 23)
            self.assertLessEqual(date.day, 31)

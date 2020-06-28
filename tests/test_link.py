from link.core import Link
from link.models.user_tokens import UserTokens
import unittest


class TestLink(unittest.TestCase):

    def test_links_build(self):
        user_token = UserTokens(stackoverflow=True)
        link = Link.builder(user_token).query("foo").page_size(5)
        first_set = set([x.preview for x in link.fetch()])
        second_set = set([x.preview for x in link.fetch()])
        third_set = set([x.preview for x in link.fetch()])
        self.assertIsNotNone(link, "link shouldnt be none")
        self.assertLessEqual(len(second_set), len(first_set))
        self.assertLessEqual(len(third_set), len(second_set))
        self.assertNotEqual(first_set, second_set)
        self.assertNotEqual(third_set, second_set)

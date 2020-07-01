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

    def test_all_atributes_are_set(self):

        user_token = UserTokens(
            stackoverflow="not really needed for stackoverflow to work")
        link = Link.builder(user_token).query("foo").page_size(1)
        result = link.fetch()[0]

        self.assertIsNotNone(result.link)
        self.assertIsNotNone(result.preview)
        self.assertIsNotNone(result.date)
        self.assertIsNotNone(result.source)

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

    def test_github_works(self):

        user_token = UserTokens(
            github="this isn't really needed but needed for private results")
        link = Link.builder(user_token).query("python").page_size(6)

        results = link.fetch()

        self.assertGreaterEqual(len(results), 0)
        self.assertEqual(len(results), 6)

        date = results[0].date
        link = results[0].link
        preview = results[0].preview
        source = results[0].source

        self.assertIsNotNone(date)
        self.assertIsNotNone(link)
        self.assertIsNotNone(preview)
        self.assertIsNotNone(source)

    def test_both_github_and_stackoverflow(self):

        user_token = UserTokens(stackoverflow="foobar", github="fizzbuzz")
        link = Link.builder(user_token).query("python").page_size(12)

        results = link.fetch()
        github_count = len([x for x in results if x.source == "github"])
        so_count = len([x for x in results if x.source == "stackoverflow"])

        self.assertEqual(github_count, 6)
        self.assertEqual(so_count, 6)
        self.assertEqual(len(results), 12)

        second_set_results = link.fetch()

        self.assertNotEqual(second_set_results, results)
        github_count = len([x for x in results if x.source == "github"])
        so_count = len([x for x in results if x.source == "stackoverflow"])

        self.assertEqual(github_count, 6)
        self.assertEqual(so_count, 6)
        self.assertEqual(len(results), 12)

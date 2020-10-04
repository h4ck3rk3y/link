from link.core import Link
from link.models.user_tokens import UserTokens, UserToken
from link.searchers.base_searcher import BaseSearcher
from link.searchers.constants import GITHUB_QUALIFIERS
import unittest
from datetime import datetime
import pickle


class TestLink(unittest.TestCase):

    def test_links_build(self):
        user_token = UserTokens(
            {"stackoverflow": UserToken(token="")})
        link = Link.builder(user_token).query("foo").page_size(5)
        first_set = set([x.title for x in link.fetch()])
        second_set = set([x.title for x in link.fetch()])
        third_set = set([x.title for x in link.fetch()])
        self.assertIsNotNone(link, "link shouldnt be none")
        self.assertLessEqual(len(second_set), len(first_set))
        self.assertLessEqual(len(third_set), len(second_set))
        self.assertNotEqual(first_set, second_set)
        self.assertNotEqual(third_set, second_set)

    def test_all_atributes_are_set(self):

        user_token = UserTokens(
            {"stackoverflow": UserToken(token="")})
        link = Link.builder(user_token).query("foo").page_size(1)

        result = link.fetch()
        self.assertEqual(len(result), 1)
        result = result[0]

        self.assertIsNotNone(result.link)
        self.assertIsNotNone(result.preview)
        self.assertIsNotNone(result.date)
        self.assertIsNotNone(result.source)
        self.assertIsNotNone(result.title)

    def test_github_works(self):

        user_token = UserTokens({
            "github": UserToken(token="")})
        link = Link.builder(user_token).query("python").page_size(6)

        results = link.fetch()

        self.assertGreaterEqual(len(results), 0)
        self.assertEqual(len(results), 6)

        date = results[0].date
        link = results[0].link
        source = results[0].source
        title = results[0].title

        self.assertIsNotNone(date)
        self.assertIsNotNone(link)
        self.assertIsNotNone(source)
        self.assertIsNotNone(title)

    def test_both_github_and_stackoverflow(self):

        user_token = UserTokens({"stackoverflow": UserToken(
            token=""), "github": UserToken(token="")})
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

    def test_next_previous(self):

        user_token = UserTokens({"stackoverflow": UserToken(token="")})
        link = Link.builder(user_token).query("python").page_size(12)

        first_result_a = link.fetch()
        second_result_a = link.fetch()

        first_result_b = link.previous()
        second_result_b = link.fetch()

        third_results_a = link.fetch()
        fourth_result_a = link.fetch()
        fifth_result_a = link.fetch()
        sixth_result_a = link.fetch()

        fifth_result_b = link.previous()
        fourth_result_b = link.previous()
        third_result_b = link.previous()

        self.assertEqual(first_result_a, first_result_b)
        self.assertEqual(second_result_a, second_result_b)
        self.assertEqual(third_results_a, third_result_b)
        self.assertEqual(fourth_result_a, fourth_result_b)
        self.assertEqual(fifth_result_a, fifth_result_b)

        self.assertNotEqual(third_results_a, first_result_a)
        self.assertNotEqual(second_result_a, third_results_a)
        self.assertNotEqual(first_result_a, second_result_a)
        self.assertNotEqual(sixth_result_a, fifth_result_a)
        self.assertNotEqual(fifth_result_a, fourth_result_a)
        self.assertNotEqual(fourth_result_a, third_results_a)

    def tets_odd_number_of_pulls(self):

        user_token = UserTokens({"stackoverflow": UserToken(token="")})
        link = Link.builder(user_token).query("python").page_size(13)

        result = link.fetch()

        self.assertEqual(len(result), 13)

    def test_github_urls_are_not_api_urls(self):

        user_token = UserTokens(
            {"github": UserToken(token="")})
        link = Link.builder(user_token).query("python").page_size(20)

        result = link.fetch()

        urls = [x.link for x in result]

        categories = set([x.category for x in result])

        self.assertGreater(len(categories), 1)
        self.assertNotEqual(len(urls), 0)

        self.assertNotEqual(len(urls), 0)

        for url in urls:
            self.assertTrue(url.startswith("https://github.com"))

    @unittest.skip("only run in person with token")
    def test_slack(self):

        user_token = UserTokens({"slack": UserToken(token="")})

        link = Link.builder(user_token).query("memes").page_size(5)
        result = link.fetch()

        self.assertGreaterEqual(len(result), 1)

    @unittest.skip("this test should be done in person with an api key and token")
    def test_trello_cards(self):

        token = ""
        key = ""
        user_token = UserTokens(
            {"trello": UserToken(token=token, username=key)})

        link = Link.builder(user_token).query("Neural Network").page_size(10)
        result = link.fetch()

        result = sorted(result, key=lambda x: x.date)

        self.assertGreaterEqual(len(result), 1)

        self.assertEqual(
            result[0].preview, "This engine would combine scores of all the three neural networks, and return an overall ranking. The scores would be nothing but the relevance score of every <image, tag> pair")
        self.assertEqual(
            result[0].title, "Engine to serve relevant search results")
        self.assertEqual(result[0].date.year, 2018)
        self.assertEqual(result[0].link, "https://trello.com/c/pOL4lk4a")

    def test_different_non_github_queries(self):
        test_cases = [
            "is:public tomatoes are red user:psdh",
            "tomatoes are red",
            "memes user:psdh",
            "memes is:private",
            "foobar is:public user:h4ck3rk3y can be user:psdh org:darkstark going",
            "foobar is:public going",
            "tomatoes are red review:changes_requested",
            "reviewed-by:tomatoes are red",
            "user: psdh is sodhi",
            "review-requested:sodhi is psdh",
        ]

        expected_results = [
            "tomatoes are red",
            "tomatoes are red",
            "memes",
            "memes",
            "foobar can be going",
            "foobar going",
            "tomatoes are red",
            "are red",
            "user: psdh is sodhi",
            "is psdh",
        ]

        for index, test in enumerate(test_cases):
            searcher = BaseSearcher(token="", username="",
                                    query=test, per_page=15, source_result=None, name="foo")

            self.assertEqual(
                expected_results[index], searcher.query)

    def test_github_qualifiers_for_github(self):
        test_cases = [
            "is:public tomatoes are red user:psdh",
            "tomatoes are red",
            "memes user:psdh",
            "memes is:private",
            "foobar is:public user:h4ck3rk3y can be user:psdh org:darkstark going",
            "foobar is:public going",
            "tomatoes are red review:changes_requested",
            "reviewed-by:tomatoes are red",
            "user: psdh is sodhi",
            "review-requested:sodhi is psdh",
        ]

        for test in test_cases:
            searcher = BaseSearcher(token="", username="",
                                    query=test, per_page=15, source_result=None, name="foo", acceptable_qualifiers=GITHUB_QUALIFIERS)

            self.assertEqual(
                test, searcher.query)

    @unittest.skip("Needs a working gitlab token")
    def test_gitlab_works(self):

        user_token = UserTokens({
            "gitlab": UserToken(token="")})
        link = Link.builder(user_token).query("file").page_size(6)

        results = link.fetch()

        self.assertEqual(len(results), 6)

        date = results[0].date
        link = results[0].link
        preview = results[0].preview
        source = results[0].source
        title = results[0].title

        self.assertIsNotNone(date)
        self.assertIsNotNone(link)
        self.assertIsNotNone(preview)
        self.assertIsNotNone(source)
        self.assertIsNotNone(title)

    @unittest.skip("This needs to run with gyanis token and username")
    def test_gitlab_works_user_only(self):

        user_token = UserTokens({
            "gitlab": UserToken(token="", username="")})
        link = Link.builder(user_token).query(
            "nisploit").user_only(True).page_size(6)

        results = link.fetch()

        self.assertEqual(len(results), 1)

        date = results[0].date
        link = results[0].link
        preview = results[0].preview
        source = results[0].source
        title = results[0].title

        self.assertIsNotNone(date)
        self.assertIsNotNone(link)
        self.assertIsNotNone(preview)
        self.assertIsNotNone(source)
        self.assertIsNotNone(title)

    def test_link_pickles(self):
        user_token = UserTokens(
            {"stackoverflow": UserToken(token="")})
        link = Link.builder(user_token).query("foo").page_size(5)
        dumpd = pickle.dumps(link)
        self.assertIsNotNone(dumpd)

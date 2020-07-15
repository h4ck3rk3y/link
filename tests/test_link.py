from link.core import Link
from link.models.user_tokens import UserTokens, UserToken
import unittest
from datetime import datetime
import requests
from pstats import Stats
import cProfile

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}


class TestLink(unittest.TestCase):

    def setUp(self):
        """init each test"""
        self.pr = cProfile.Profile()
        self.pr.enable()
        print("\n<<<---")

    def tearDown(self):
        """finish any test"""
        p = Stats(self.pr)
        p.strip_dirs()
        p.sort_stats('tottime')
        p.print_stats()
        print("\n--->>>")

    def test_fire_forget(self):
        user_token = UserTokens(stackoverflow=UserToken(
            token=""), github=UserToken(token=""))
        link = Link.builder(user_token).query("python").page_size(12)
        now = datetime.now()
        result = link.fetch()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(result), 12)
        while i:
            self.assertLessEqual(time_elapsed, i)
            i = i / 2.0
            if i < 0.0625:
                break

    def test_fire_forget_round_two(self):
        user_token = UserTokens(stackoverflow=UserToken(
            token=""), github=UserToken(token=""))
        link = Link.builder(user_token).query("golang").page_size(12)
        now = datetime.now()
        result = link.fetch()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(result), 12)
        i = 2.0
        self.assertEqual(len(result), 12)
        while i:
            self.assertLessEqual(time_elapsed, i)
            i = i / 2.0
            if i < 0.0625:
                break

    def test_fire_forget_terminal(self):
        user_token = UserTokens(stackoverflow=UserToken(
            token=""), github=UserToken(token=""))
        link = Link.builder(user_token).query("java").page_size(12)
        now = datetime.now()
        result = link.fetch()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(result), 12)
        i = 2.0
        self.assertEqual(len(result), 12)
        while i:
            self.assertLessEqual(time_elapsed, i)
            i = i / 2.0
            if i < 0.0625:
                break

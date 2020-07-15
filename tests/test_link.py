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

    def test_a_token_request_that_runs_before_everyone(self):
        for query in ["python", "java", "golang", "c++", "ocaml"]:
            now = datetime.now()
            response = requests.get(
                "https://api.github.com/search/issues", headers=HEADERS, params={"q": query, "per_page": 12})
            data = response.json()
            later = datetime.now()
            time_elapsed = later - now
            time_elapsed = time_elapsed.total_seconds()
            self.assertEqual(len(data['items']), 12)
            i = 2.0
            while True:
                if i < 0.0625:
                    break
                self.assertLessEqual(time_elapsed, i)
                i = i/2.0

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

    def test_yolo_both_github_and_stackoverflow(self):

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
        while True:
            if i < 0.0625:
                break
            self.assertLessEqual(time_elapsed, i)
            i = i/2.0

    def test_just_github(self):

        user_token = UserTokens(github=UserToken(token=""))
        link = Link.builder(user_token).query("python").page_size(12)
        now = datetime.now()
        result = link.fetch()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(result), 12)
        while True:
            if i < 0.03125:
                break
            self.assertLessEqual(time_elapsed, i)
            i = i/2.0

    def test_just_stackoverflow(self):

        user_token = UserTokens(stackoverflow=UserToken(
            token=""))
        link = Link.builder(user_token).query("python").page_size(12)
        now = datetime.now()
        result = link.fetch()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(result), 12)
        while True:
            if i < 0.0625:
                break
            self.assertLessEqual(time_elapsed, i)
            i = i/2.0

    def test_yz_token_request_that_runs_before_everyone(self):
        now = datetime.now()
        response = requests.get(
            "https://api.github.com/search/issues", headers=HEADERS, params={"q": "python", "per_page": 12})
        data = response.json()
        later = datetime.now()
        time_elapsed = later - now
        time_elapsed = time_elapsed.total_seconds()
        i = 2.0
        self.assertEqual(len(data['items']), 12)
        while True:
            if i < 0.0625:
                break
            self.assertLessEqual(time_elapsed, i)
            i = i/2.0

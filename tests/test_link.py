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

    def test_1_python(self):
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

    def test_2_golang(self):
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

    def test_3_python(self):
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
        i = 2.0
        self.assertEqual(len(result), 12)
        while i:
            self.assertLessEqual(time_elapsed, i)
            i = i / 2.0
            if i < 0.0625:
                break

    def test_4_golang(self):
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

    def test_5_java(self):
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

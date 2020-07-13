from link.core import Link
from link.models.user_tokens import UserTokens, UserToken
import unittest
from datetime import datetime


class TestLink(unittest.TestCase):

    def test_warmup_the_request(self):
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

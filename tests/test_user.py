import unittest
from link.models.user_tokens import UserTokens


class TestUser(unittest.TestCase):

    def test_slack(self):
        user = UserTokens()
        user.slack = "foobar"
        self.assertEqual(user.slack, "foobar")

    def test_github(self):
        user = UserTokens()
        user.github = "fizzbuzz"
        self.assertEqual(user.github, "fizzbuzz")

    def test_stackoverflow(self):
        user = UserTokens()
        user.stackoverflow = "overflow"
        self.assertEqual(user.stackoverflow, "overflow")

    def test_trello(self):
        user = UserTokens()
        user.trello = "trello"
        self.assertEqual(user.trello, "trello")

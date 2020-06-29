import unittest
from link.models.sources_enabled import SourcesEnabled


class SourceEnabledTests(unittest.TestCase):

    def test_source_enabled(self):
        sources_enabled = SourcesEnabled()
        sources_enabled.stackoverflow = False
        sources_enabled.github = True
        sources_enabled.trello = False
        sources_enabled.slack = False

        self.assertTrue(sources_enabled.github)
        self.assertFalse(sources_enabled.trello)
        self.assertFalse(sources_enabled.stackoverflow)
        self.assertFalse(sources_enabled.slack)

from link.searchers.link_bitbucket_code import get_preview, get_highlighted_lines, get_link
import unittest

matches = {"content_matches": [
    {
        "lines": [
            {
                "line": 1,
                "segments": [
                    {
                        "text": "function",
                        "match": True
                    },
                    {
                        "text": "  sum (x, y) {"
                    }
                ]
            },
            {
                "line": 3,
                "segments": [
                    {
                        "text": "}"
                    }
                ]
            },
            {
                "line": 5,
                "segments": [
                    {
                        "text": "function",
                        "match": True
                    },
                    {
                        "text": "  diff (x, y) {"
                    }
                ]
            }
        ]
    }
],
    "path_matches": []}


class TestBitbucketHelpers(unittest.TestCase):

    def test_get_preview(self):
        preview = get_preview(matches)
        expected_result =\
            "<span class=\"highlight\">function</span>\n  sum (x, y) {\n}\n<span " \
            "class=\"highlight\">function</span>\n  diff (x, y) {"

        self.assertEqual(preview, expected_result)

        matches["path_matches"] = [
            {
                "text": "index",
                "match": True
            },
            {
                "text": ".js",
            }
        ]

        preview = get_preview(matches)
        expected_result = "<span class=\"highlight\">index</span>.js"
        self.assertEqual(preview, expected_result)

    def test_get_highlighted_links(self):
        highlighted_lines = get_highlighted_lines(matches)
        expected_result = '1,5'
        self.assertEqual(highlighted_lines, expected_result)

    def test_get_link(self):
        web_link = get_link("https://api.bitbucket.org/2.0/repositories/bhavdeepdhanjal/public_test/src"
                            "/833a370c28b09525b448c8ca42a05635b1d465ca/index.js")
        expected_link = "https://bitbucket.org/bhavdeepdhanjal/public_test/src" \
                        "/833a370c28b09525b448c8ca42a05635b1d465ca/index.js"
        self.assertEqual(web_link, expected_link)

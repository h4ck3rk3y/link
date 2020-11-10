from .base_searcher import BaseSearcher
from ..models.results import SingleResult, Page
from urllib.parse import quote, urlparse
from datetime import timedelta, datetime

"""
API and example output can be found here:
https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/search/code

Request Limits:
https://support.atlassian.com/bitbucket-cloud/docs/api-request-limits/
"""


class BitbucketCodeSearcher(BaseSearcher):
    source = "bitbucket"
    name = "bitbucket"
    url = "https://api.bitbucket.org/2.0/workspaces/%s/search/code"
    user_priority = False

    def __init__(self, user_token, query, per_page, source_result, user_only):
        self.url = self.url % quote(user_token.extra_data["uuid"])
        super().__init__(user_token.token, user_token.username, query, per_page,
                         source_result, self.name, user_only)

    def construct_request_parts(self, page):
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.token}"}
        payload = {
            "search_query": self.query,
            "pagelen": self.per_page,
            "page": page
        }
        return self.url, payload, headers

    def validate(self, response):
        banned_until = None
        if response.status_code != 200:
            if response.status_code == 429:
                banned_seconds = int(response.headers['Retry-After'])
                banned_until = datetime.now() + timedelta(seconds=banned_seconds)
            return False, banned_until
        return True, banned_until

    def parse(self, response):
        if response.get("next"):
            self.exhausted = True

        result_page = Page()
        for entry in response["values"]:
            href = get_link(entry["file"]["links"]["self"]["href"])
            preview = get_preview(entry)
            category = entry["type"]
            title = entry["file"]["path"]
            link = f"{href}#lines-{get_highlighted_lines(entry)}"
            single_result = SingleResult(
                preview, link, self.source, None, category, title)
            result_page.add(single_result)
        return result_page


def get_preview(matches):
    # Assumption(@alivenotions): If we get a file path match, don't care about
    # the line matches as those will be highlighted in the file anyway
    # In the future, can send both
    if len(matches["path_matches"]) > 0:
        preview = []
        for entry in matches["path_matches"]:
            text = wrap_with_highlight(entry["text"]) if 'match' in entry else entry["text"]
            preview.append(text)
        return ''.join(preview)

    preview = []
    matched_lines = matches["content_matches"][0]["lines"]
    for entry in matched_lines:
        for segment in entry["segments"]:
            text = wrap_with_highlight(segment["text"]) if 'match' in segment else segment["text"]
            preview.append(text)
    return '\n'.join(preview[:8])


def wrap_with_highlight(str):
    return f"<span class=\"highlight\">{str}</span>"


def get_highlighted_lines(matches):
    line = []
    if len(matches["content_matches"]) > 0:
        matched_lines = matches["content_matches"][0]["lines"]
        for entry in matched_lines:
            for segment in entry["segments"]:
                if 'match' in segment:
                    line.append(entry["line"])
                    break
    return ','.join(map(str, line))


def get_link(url):
    parsed = urlparse(url)
    http_scheme = parsed.scheme
    base_url = "bitbucket.org"
    web_ui_path = parsed.path.split('/')[3:]

    return f"{http_scheme}://{base_url}/{'/'.join(web_ui_path)}"

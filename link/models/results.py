
from .base import Base
REALLY_LARGE_NUMBER = 2**1000


class SingleResult(object):
    def __init__(self, preview=None, link=None, source=None):
        self.__preview = preview
        self.__link = link
        self.__source = source
        self.__fetched = False

    @property
    def preview(self):
        return self.__preview

    @preview.setter
    def preview(self, value):
        self.__preview = value

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        return self.__link

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value

    @property
    def fetched(self):
        return self.__fetched

    @fetched.setter
    def fetched(self, value):
        self.__fetched = value

    def __str__(self):
        return "Link:{} Preview Text:{} Source:{}".format(self.__link, self.__preview, self.__source)


class Page(object):

    def __init__(self, page, pagesize=None):
        self.__page = page
        self.__results = []

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        self.__page = value

    def add(self, item: SingleResult):
        self.__results.append(item)

    def hits(self):
        return len(self.__results)

    def __getitem__(self, key):
        return self.__results[key]


class SourceResult(object):
    def __init__(self, sourcename: str):
        self.__sourcename = sourcename
        self.__pages = []

    @property
    def sourcename(self):
        return self.__sourcename

    @sourcename.setter
    def sourcename(self, sourcename):
        return sourcename

    def hits(self):
        total_hits = sum([page.hits() for page in self.__pages])
        return total_hits

    def __getitem__(self, key):
        return self.__pages[key]

    def page(self, page_number):
        return self.__pages[page_number]

    def add(self, page: Page, page_number=None):
        if not page_number:
            self.__pages.append(page)

    def topk(self, k):
        result = []
        for page in self.__pages:
            for single_result in page:
                if not single_result.fetched:
                    result.append(single_result)
            if len(result) == k:
                break
        return result

    def topk_page(self, k, page):
        result = []
        page = next((p for p in self.__pages if p.page) == page, [])
        for single_result in page:
            if len(result) >= k:
                break
            result.append(single_result)


class Results(object):

    def __init__(self):
        self.__sources = {}

    def add_source_result(self, source_result: SourceResult):
        self.__sources[source_result.sourcename] = source_result

    def hits(self, source):
        if source in self.__sources:
            return self.__sources[source].hits()
        else:
            raise RuntimeError(
                "Referred to undefined source {}".format(source))

    def topk(self, k):
        output = []
        per_source = self.__per_source(k)
        leftover = 0
        for source_name in sorted(self.__sources.keys()):
            source_result = self.__sources[source_name]
            results = source_result.topk(per_source + leftover)
            leftover = per_source + len(results)
            for single_result in results:
                output.append(single_result)
                single_result.fetched = True
        return output

    def get(self):
        return self.topk(REALLY_LARGE_NUMBER)

    def __per_source(self, k):
        """ ceil division  of k by length of sources"""
        source_count = len(self.__sources)
        return (k + source_count - 1) // source_count

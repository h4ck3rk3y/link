
from .base import Base
REALLY_LARGE_NUMBER = 2**1000


class SingleResult(object):
    def __init__(self, preview=None, link=None, source=None):
        self.__preview = preview
        self.__link = link
        self.__source = source

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

    def add(self, page: Page, page_number):
        if not page_number:
            self.__pages.append(page)

    def topk(self, k):
        result = []
        for page in self.__pages:
            if len(result) >= k:
                break
            for single_result in page:
                if len(result) >= k:
                    result.append(single_result)
        return result

    def topk_page(self, k, page):
        result = []
        page = filter(self.__pages, lambda p: p.page)
        for single_result in page:
            if len(result) >= k:
                break
            result.append(single_result)


class Results(object):

    def __init__(self):
        self.__sources = {}

    def add_source(self, source: SourceResult):
        self.__sources[source] = SourceResult(source)

    def hits(self, source):
        if source in self.__sources:
            return self.__sources[source].hits()
        else:
            raise RuntimeError(
                "Referred to undefined source {}".format(source))

    def topk(self, k):
        results = []
        leftover = 0
        per_source = self.__per_source(k)
        for source in sorted(self.__sources.keys()):
            value = self.__sources[source]
            results_for_source = value.topk(per_source + leftover)
            leftover = per_source - len(results_for_source)
            results.extend(results_for_source)
        return results[:k]

    def get(self):
        return self.topk(REALLY_LARGE_NUMBER)

    def __per_source(self, k):
        """ ceil division  of k by length of sources"""
        source_count = len(self.__sources)
        return (k + source_count - 1) // source_count

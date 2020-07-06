
from .base import Base
REALLY_LARGE_NUMBER = 2**1000


class SingleResult(object):
    def __init__(self, preview=None, link=None, source=None, date=None, category=None):
        self.__preview = preview
        self.__link = link
        self.__source = source
        self.__fetched = False
        self.__date = date
        self.__category = None

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

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value

    def __str__(self):
        return f"Link:{self.__link} Preview Text:{self.__preview} Source:{self.__source} Date:{self.__date} Category:{self.__category}"

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        json_value = {
            "preview": self.preview,
            "link": self.link,
            "source": self.source,
            "date": self.date.timestamp(),
        }

        if (self.category):
            json_value["category"] = self.category

        return json_value


class Page(object):

    def __init__(self, page, pagesize=None):
        self.__page = page
        self.__results = []

    def add(self, item: SingleResult):
        self.__results.append(item)

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

    def add(self, page: Page, page_number=None):
        if not page_number:
            self.__pages.append(page)

    def topk(self, k):
        result = []
        for page in self.__pages:
            for single_result in page:
                if len(result) == k:
                    break
                if not single_result.fetched:
                    result.append(single_result)

        return result


class Results(object):

    def __init__(self):
        self.__sources = {}

    def add_source_result(self, source_result: SourceResult):
        self.__sources[source_result.sourcename] = source_result

    def topk(self, k):
        output = []
        per_source = self.__per_source(k)
        leftover = 0
        for source_name in sorted(self.__sources.keys()):
            source_result = self.__sources[source_name]
            results = source_result.topk(per_source + leftover)
            leftover = per_source - len(results)
            for single_result in results:
                if len(output) == k:
                    break
                output.append(single_result)
                single_result.fetched = True
        return output

    def __per_source(self, k):
        """ ceil division  of k by length of sources"""
        source_count = len(self.__sources)
        return (k + source_count - 1) // source_count

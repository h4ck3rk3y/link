from typing import List


class SourcesEnabled:

    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    def __str__(self):
        as_str = []
        for source in self.tokens:
            as_str.append(f"{source} enabled")
        return " ".join(as_str)

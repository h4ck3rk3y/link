from .base import Base


class SourcesEnabled(Base):

    def __init__(self, slack=True, github=True, stackoverflow=True, trello=True):
        super().__init__(slack, github, trello, stackoverflow)

    def __to__str(self):
        return f"slack:{self.slack} github:{self.github} trello:{self.trello} stackoverflow:{self.stackoverflow}"

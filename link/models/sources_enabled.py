from .base import Base


class SourcesEnabled(Base):

    def __init__(self, slack=True, github=True, stackoverflow=True, trello=True):
        super().__init__(slack, github, trello, stackoverflow)

    def __to__str(self):
        return "slack:{} github:{} trello:{} stackoverflow:{}".format(self.slack, self.github, self.trello, self.stackoverflow)

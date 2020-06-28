from .base import Base


class UserTokens(Base):

    def __init__(self, slack=None, github=None, trello=None, stackoverflow=None):
        super().__init__(slack, github, trello, stackoverflow)

    def __str__(self):
        return "User tokens enabled for slack:{} github:{} trello:{} stackoverflow:{}".format(self.slack != None, self.github != None, self.trello != None, self.stackoverflow != None)

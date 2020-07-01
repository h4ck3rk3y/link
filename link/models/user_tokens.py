from .base import Base


class UserTokens(Base):

    def __init__(self, slack=None, github=None, trello=None, stackoverflow=None):
        super().__init__(slack, github, trello, stackoverflow)

    def __str__(self):
        return f"User tokens enabled for slack:{self.slack!=None} github:{self.github!=None} trello:{self.trello!=None} stackoverflow:{self.stackoverflow!=None}"

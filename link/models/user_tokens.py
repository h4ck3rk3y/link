from .base import Base


class UserToken(object):

    def __init__(self, token: str = None, username: str = None):
        self.__username = username
        self.__token = token

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    def __str__(self):
        return "Username: {self.__username}"


class UserTokens(Base):

    def __init__(self, slack: UserToken = None, github: UserToken = None, trello: UserToken = None, stackoverflow: UserToken = None):
        super().__init__(slack, github, trello, stackoverflow)

    def __str__(self):
        return f"User tokens enabled for slack:{self.slack!=None} github:{self.github!=None} trello:{self.trello!=None} stackoverflow:{self.stackoverflow!=None}"

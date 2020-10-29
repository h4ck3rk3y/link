from typing import Dict


class UserToken(object):

    def __init__(self, token: str = None, username: str = None, extra_data: dict = None):
        self.__username = username
        self.__token = token
        self.__extra_data = extra_data

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

    @property
    def extra_data(self):
        return self.__extra_data

    @extra_data.setter
    def extra_data(self, value):
        self.__extra_data = value

    def __str__(self):
        return "Username: {self.__username}"


class UserTokens:

    def __init__(self, tokens: Dict[str, UserToken]):
        self.tokens = tokens

    def __str__(self):
        as_str = []
        for source in self.tokens.keys():
            as_str.append(f"{source} enabled")
        return " ".join(as_str)

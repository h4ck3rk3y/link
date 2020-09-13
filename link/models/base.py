class Base(object):

    def __init__(self, slack=None, github=None, trello=None, stackoverflow=None, gitlab=None):
        self.__slack = slack
        self.__github = github
        self.__trello = trello
        self.__stackoverflow = stackoverflow
        self.__gitlab = gitlab

    @property
    def slack(self):
        return self.__slack

    @slack.setter
    def slack(self, slack):
        self.__slack = slack

    @property
    def github(self):
        return self.__github

    @github.setter
    def github(self, github):
        self.__github = github

    @property
    def trello(self):
        return self.__trello

    @trello.setter
    def trello(self, trello):
        self.__trello = trello

    @property
    def stackoverflow(self):
        return self.__stackoverflow

    @stackoverflow.setter
    def stackoverflow(self, stackoverflow):
        self.__stackoverflow = stackoverflow

    @property
    def gitlab(self):
        return self.__gitlab

    @gitlab.setter
    def gitlab(self, gitlab):
        self.__gitlab = gitlab

    def __repr__(self):
        return self.__str__()

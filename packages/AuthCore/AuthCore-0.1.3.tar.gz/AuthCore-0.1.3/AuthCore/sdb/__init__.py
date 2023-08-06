import json


class DBInterface:
    def __insert__(self, key, value):
        raise NotImplementedError

    def __select__(self, key):
        raise NotImplementedError

    def __update__(self, key, value):
        raise NotImplementedError

    def __remove__(self, key):
        raise NotImplementedError



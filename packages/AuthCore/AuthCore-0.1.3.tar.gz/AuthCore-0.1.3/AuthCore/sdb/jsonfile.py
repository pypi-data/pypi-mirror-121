from . import DBInterface
import json


class JsonDBInterface(DBInterface, dict):
    def __init__(self, table_name, path="./"):
        super().__init__()
        self.path = path
        self.table_name = table_name
        self.update(self.__load__(path=path, table_name=table_name))

    def dump(self):
        self.__write__(self.copy(), self.path, self.table_name)

    def __insert__(self, key, value, e=RuntimeError()):
        if key in self.keys():
            raise e
        else:
            self.__setitem__(key, value)
            self.dump()

    def __select__(self, key):
        if key not in self.keys():
            return None
        else:
            return self.__getitem__(key)

    def __update__(self, key, value):
        self.__setitem__(key, value)
        self.dump()

    def __remove__(self, key):
        self.__delitem__(key)
        self.dump()

    ##
    @staticmethod
    def __load__(path, table_name):
        try:
            with open(f"{path}{table_name}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {}

    @staticmethod
    def __write__(data, path, table_name):
        with open(f"{path}{table_name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

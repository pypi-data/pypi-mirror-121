# client = pymongo.MongoClient("mongodb+srv://root:<password>@cluster0.ooglx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
import pymongo
from . import DBInterface


class MongoDBInterface(DBInterface, dict):
    def __init__(self, account_label, user="root", pws="root", collection="auth"):
        super().__init__()
        self.url = f"mongodb://{user}:{pws}@cluster0-shard-00-00.{account_label}.mongodb.net:27017,cluster0-shard-00-01.{account_label}.mongodb.net:27017,cluster0-shard-00-02.ooglx.{account_label}.net:27017/{collection}?ssl=true&authSource=admin"
        self.table = None
        self.connect = None

    def select_table(self, database, table_name):
        # self.table = self.client[database][table_name]
        self.table = (database, table_name)

    def get_connect(self):
        if self.table is None:
            raise RuntimeError("NO SELECT TABLE")
        self.connect = pymongo.MongoClient(self.url)
        database, table_name = self.table
        return self.connect[database][table_name]

    def removed_connect(self):
        if self.connect is None:
            return
        self.connect.close()
        self.connect = None

    def __insert__(self, key, value, e=RuntimeError("key exist")):
        if self.__select__(key) is None:
            cli = self.get_connect()
            result = cli.insert_one({
                "key": key,
                **value
            })
            self.removed_connect()
            return result
        else:
            raise e

    def __select__(self, key):
        cli = self.get_connect()
        result = cli.find_one({'key': key})
        if result is None:
            return result
        result = dict(result)
        del result["_id"]

        self.removed_connect()
        return result

    def __update__(self, key, value):
        if self.__select__(key) is None:
            raise RuntimeError(f"key is not existed: {key}")
        select_filter = {"key": key}
        value = {"$set": value}

        cli = self.get_connect()
        result = cli.update_one(select_filter, value)

        self.removed_connect()
        return result

    def __remove__(self, key):
        if self.__select__(key) is None:
            raise RuntimeError(f"key is not existed: {key}")

        select_filter = {"key": key}
        cli = self.get_connect()
        result = cli.delete_one(select_filter)
        self.removed_connect()
        return result

    def dump(self):
        cli = self.get_connect()
        result = cli.find()
        if result is None:
            return result

        self.removed_connect()
        return result

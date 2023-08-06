from .__rsa__ import keyGen, encrypt, decrypt
from .sdb.jsonfile import JsonDBInterface as JDB
from .sdb.mongo import MongoDBInterface as MDB
import uuid
import json
import time


class DecryptITF:
    @staticmethod
    def decrypt(*args, **kwargs):
        return decrypt(*args, **kwargs)


class MemberSystem:
    def signup_platform(self, label=None):
        label = str(uuid.uuid4()) if label is None else label
        encode_key, decode_key = keyGen()
        encode_key, decode_key = [int(i) for i in encode_key], [int(i) for i in decode_key]

        self.__set_rsa_key_of_platform__(label, encode_key, decode_key)
        return decode_key, label

    def signup_user(self, account, pws):
        account, pws = self.__hash_login_info__(account, pws)
        self.__set_new_user__(account, pws)

    def login_user(self, label, account, pws, encode=True):
        account, pws = self.__hash_login_info__(account, pws)
        return self.__get_user_by_account_and_pws__(label, account, pws, encode)

    def update_user(self, account, pws, **kwargs):
        account, pws = self.__hash_login_info__(account, pws)
        self.__set_user_info__(account=account, pws=pws, **kwargs)

    def delete_user(self, account, pws):
        account, pws = self.__hash_login_info__(account, pws)
        self.__del_user_by_account_and_pws__(account=account, pws=pws)

    ##
    def __hash_login_info__(self, account, pws):
        salted_account = self.salt_func(self.salt_func_namespace, account)
        salted_pws = self.salt_func(self.salt_func_namespace, pws)
        return str(salted_account), str(salted_pws)

    def __set_rsa_key_of_platform__(self, label, encode_key, decode_key):

        data = {
            "encode_key": encode_key,
            "decode_key": decode_key
        }
        self.DB_platform.__insert__(label, data, RuntimeError(f"the label is exist.: {label}"))

    def __get_platform_key_by_label__(self, label):
        return self.DB_platform.__select__(label)

    def __set_new_user__(self, account, pws):
        data = {
            "pws": pws,
            "uuid": str(uuid.uuid4())
        }
        self.DB_user.__insert__(key=account, value=data,
                                e=RuntimeError(f"the account is exist.: {account}"))

    def __set_user_info__(self, account, pws, **kwargs):
        source_info = self.__get_user_by_account_and_pws__(label=None, account=account, pws=pws, encode=False)
        source_info.update(kwargs)
        #
        self.DB_user.__update__(account, source_info)
        #

    def __get_user_by_account_and_pws__(self, label, account, pws, encode=True):
        user = self.DB_user.__select__(account)
        if user is None:
            raise RuntimeError(f"the account is not exist.: {account}")
        if user['pws'] != pws:
            raise RuntimeError(f"the passwords is not exist.: {account}")
        user = user.copy()

        #
        if encode:
            rsa_key = self.__get_platform_key_by_label__(label)
            if rsa_key is None:
                raise RuntimeError(f"the label is not exist.: {label}")
            del user['pws']
            return encrypt(rsa_key['encode_key'], json.dumps(user))
        else:
            return user

    def __del_user_by_account_and_pws__(self, account, pws):
        _ = self.__get_user_by_account_and_pws__(label=None, account=account, pws=pws, encode=False)
        self.DB_user.__remove__(account)


class SimpleMemberSystem(MemberSystem):
    def __init__(self, db_file_path="./", uuid_hash="9b542d3a-c4d6-45ea-9408-783dca9e5f2b"):
        self.db_file_path = db_file_path
        self.DB_platform = JDB(path=db_file_path, table_name="platform")
        self.DB_user = JDB(path=db_file_path, table_name="user")
        self.salt_func = uuid.uuid5
        self.salt_func_namespace = uuid.UUID(uuid_hash)


class MongoDBMemberSystem(MemberSystem):
    def __init__(self, account_label, user, pws, collection, uuid_hash="9b542d3a-c4d6-45ea-9408-783dca9e5f2b"):
        self.DB_platform = MDB(account_label, user, pws, collection)
        self.DB_user = MDB(account_label, user, pws, collection)
        self.salt_func = uuid.uuid5
        self.salt_func_namespace = uuid.UUID(uuid_hash)

        #
        self.DB_platform.select_table("member", "platform")
        self.DB_user.select_table("member", "user")

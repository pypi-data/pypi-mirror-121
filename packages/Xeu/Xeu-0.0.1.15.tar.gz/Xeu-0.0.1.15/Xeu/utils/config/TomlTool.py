import collections
from typing import Dict

import toml

from Xeu.configure.base import Config, ConfigBase
from Xeu.configure.collection import Collection
from Xeu.utils.config.base import ConfigFileOperation


class TomlConfigFileOperation(ConfigFileOperation):

    def __init__(self, config_path: str, collection: Collection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dic = dict()
        self.toml_file_path = config_path
        self.__collection = collection

    # def __add__(self, other):
    #     self.dic.update(self.other)
    #     return self.dic

    def write(self):
        mysql_dic = {"user": "root", "password": "Aa1234"}
        mysql2_dic = {"user1": "root", "password2": "Aa1234"}
        mysql_dic.update(mysql2_dic)
        with open(self.toml_file_path, "w", encoding="utf-8") as fs:
            toml.dump(mysql_dic, fs)

    def read(self) -> ConfigBase:
        with open(self.toml_file_path, "r", encoding="utf-8") as fs:
            t_data = toml.load(fs)
        return Config(t_data, self.__collection)




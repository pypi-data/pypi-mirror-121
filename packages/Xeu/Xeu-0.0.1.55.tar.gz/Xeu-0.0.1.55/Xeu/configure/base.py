# _*_ coding:utf-8 _*_
from copy import copy
from typing import Dict
from abc import abstractmethod, ABCMeta

from Xeu.configure.collection import Collection


class ConfigBase(metaclass=ABCMeta):

    @abstractmethod
    def get_current_env_data(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def current_env_tag(self):
        pass


class Config(ConfigBase):

    def __init__(self, data: Dict, collection: Collection):
        self.data = data
        # print(__class__, "collection", id(collection))
        self.__collection = collection
        # print(__class__, "self.__collection", id(self.__collection))
        self.__collection.set("runtime", "env", self.data.get("runtime").get("env"))
        self.__collection.set("listen", "ipv4", self.data.get("listen").get(self.__collection.runtime.env)['ipv4'])
        self.__collection.set("listen", "port", self.data.get("listen").get(self.__collection.runtime.env)['port'])
        self.__collection.set("LISTEN", "ipv4", self.data.get("listen").get(self.__collection.runtime.env)['ipv4'])
        self.__collection.set("LISTEN", "port", self.data.get("listen").get(self.__collection.runtime.env)['port'])
        # Mysql
        if self.data.get("mysql", None) is not None:
            self.__collection.set("mysql", "account", self.data.get("mysql").get(self.__collection.runtime.env)['account'])
            self.__collection.set("mysql", "password", self.data.get("mysql").get(self.__collection.runtime.env)['password'])
            self.__collection.set("mysql", "ipv4", self.data.get("mysql").get(self.__collection.runtime.env)['ipv4'])
            self.__collection.set("mysql", "port", self.data.get("mysql").get(self.__collection.runtime.env)['port'])
            self.__collection.set("mysql", "database", self.data.get("mysql").get(self.__collection.runtime.env)['database'])
        # Redis
        if self.data.get("redis", None) is not None:
            self.__collection.set("redis", "account", self.data.get("redis").get(self.__collection.runtime.env)['account'])
            self.__collection.set("redis", "password", self.data.get("redis").get(self.__collection.runtime.env)['password'])
            self.__collection.set("redis", "ipv4", self.data.get("redis").get(self.__collection.runtime.env)['ipv4'])
            self.__collection.set("redis", "port", self.data.get("redis").get(self.__collection.runtime.env)['port'])
            self.__collection.set("redis", "extends", self.data.get("redis").get(self.__collection.runtime.env)['extends'])

    def get_current_env_data(self, item: str):
        return self.__collection.runtime.env

    @property
    def current_env_tag(self):
        return self.__collection.runtime.env

    @property
    def current_env_data(self):
        return self.__collection
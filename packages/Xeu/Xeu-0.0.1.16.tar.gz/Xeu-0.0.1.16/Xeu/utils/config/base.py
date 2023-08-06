# _*_ coding:utf-8 _*_
from abc import abstractmethod, ABCMeta
from Xeu.configure.base import ConfigBase


class ConfigFileOperation(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def write(self, *arg, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def read(self, *arg, **kwargs) -> ConfigBase:
        raise NotImplementedError

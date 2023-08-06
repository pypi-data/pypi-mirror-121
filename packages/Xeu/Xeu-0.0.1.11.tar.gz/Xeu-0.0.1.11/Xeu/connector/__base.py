# _*_ coding:utf-8 _*_
import redis
from abc import ABCMeta, abstractmethod


class Connection(metaclass=ABCMeta):

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass
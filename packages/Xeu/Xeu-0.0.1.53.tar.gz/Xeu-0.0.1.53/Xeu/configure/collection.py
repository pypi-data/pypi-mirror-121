"""

    存取配置文件中解析出来的字段

"""
# _*_ coding:utf-8 _*_
import collections
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Tuple


class Collection(metaclass=ABCMeta):

    @abstractmethod
    def set(self, *args, **kwargs):
        pass

    @abstractmethod
    def __getattr__(self, item) -> Any:
        pass


class _Collection(Collection):

    def __init__(self):
        super().__init__()
        self.__pool = dict()

    def set(self, item: Any, key: Any, val: Any):
        old = self.__pool.get(item)
        _temp = None
        if old:
            if isinstance(old, dict):
                pass
            elif isinstance(old, tuple):
                pass
            elif isinstance(old, int) or isinstance(old, float):
                pass
            else:
                """ 先迁移旧item 下的kv， 再更新 """
                fields = getattr(old, '_fields')
                s_fields = set(fields)
                s_fields.add(key)
                _temp = collections.namedtuple(item, list(s_fields))
                for f in fields:
                    setattr(_temp, f, getattr(old, f))
                setattr(_temp, key, val)
        else:
            _temp = collections.namedtuple(item, [key])
            setattr(_temp, key, val)
        self.__pool.update({item: _temp})

    def __getattr__(self, item) -> Any:
        return self.__pool.get(item)

Collector = _Collection()
# print("init", id(Collector))

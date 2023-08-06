# _*_ coding:utf-8 _*_
import redis

from Xeu.connector.__base import Connection


class RedisConnection(Connection):

    def __init__(self):
        self.__connector = None

    def connect(self, *args, **kwargs):
        pool = redis.ConnectionPool(
            host=kwargs['host'],
            port=kwargs['port'],
            password=kwargs['password'],
            decode_responses=True
        )
        self.__connector = redis.Redis(connection_pool=pool)
        return self.__connector

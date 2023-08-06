# _*_ coding:utf-8 _*_
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Xeu.connector.__base import Connection


class MysqlConnection(Connection):

    def __init__(self):
        self.__connector = None

    def connect(self, *args, **kwargs):
        engine = create_engine(
            f'mysql+mysqldb://root:{kwargs["host"]}@{kwargs["port"]}:{kwargs["password"]}/{kwargs["database"]}?charset=utf8',
            poolclass=None,
            pool_size=10, max_overflow=20, pool_timeout=30,
            encoding="utf-8"
        )
        _session_maker = sessionmaker(bind=engine)
        self.__connector = _session_maker()
        return self.__connector

# _*_ coding:utf-8 _*_
from abc import abstractmethod, ABCMeta


class TaskClient(metaclass=ABCMeta):

    @abstractmethod
    def create_task(self, *args, **kwargs):
        pass

    @abstractmethod
    def stop_task(self, *args, **kwargs):
        pass

    @abstractmethod
    def query_task(self, *args, **kwargs):
        pass

    @abstractmethod
    def list_tasks(self, *args, **kwargs):
        pass


class TaskServer(metaclass=ABCMeta):

    @abstractmethod
    def init_task_server(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        #
        pass

    @abstractmethod
    def stop_task_server(self, *args, **kwargs):
        pass

    @abstractmethod
    def start_task_server(self, *args, **kwargs):
        pass

# _*_ coding:utf-8 _*_
from Xeu.configure.init import Collector, Setup, BASE_CONFIG_RAW_DATA, LISTEN

from Xeu.task.task_base import TaskClient


class RedisTask(TaskClient):

    def setup_task_env(self):
        """
            初始化任务列表，分为
                待执行任务 ：
                    含任务类型，属性，执行次数
                    * 任务类型：
                    * 属性： instant_times:1 立即执行一次，
                            cron_sec:3 每三秒  cron_time:   每三秒 cron_sec:3 每三秒
                            after_sec:3 三秒后 after_min:1, after_hour:1
                待执行任务批次队列
                正在执行任务列表
                执行失败任务列表
                执行结束任务列表
        :return:
        """
        Setup(base_config=('base.toml',))
        print(Collector, id(Collector))
        print(Collector.LISTEN.port)
        print(Collector.LISTEN.ipv4)
        # a = BASE_CONFIG_RAW_DATA
        # print(BASE_CONFIG_RAW_DATA.current_env_data.redis)

    def create_task(self):
        pass

    def stop_task(self):
        pass

    def query_task(self):
        pass

    def list_tasks(self, *args, **kwargs):
        pass
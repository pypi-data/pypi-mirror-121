# _*_ coding:utf-8 _*_
from Xeu.configure.init import Setup, Collector

if __name__ == '__main__':
    Setup(base_config=('base.toml', ))
    print(Collector.runtime)
    print(Collector.listen.port)
    print(Collector.listen.ipv4)
    print(Collector.task.redis)
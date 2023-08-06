# _*_ coding:utf-8 _*_
"""
    该模块用于加载根配置文件
"""
import os
import collections
from copy import copy
from typing import Dict, Tuple, Union

from Xeu.configure.base import Config
from Xeu.configure.collection import Collector
from Xeu.utils.config.TomlTool import TomlConfigFileOperation
from Xeu.utils.config.base import ConfigFileOperation

BASE_CONFIG_FILE = ''
BASE_CONFIG_DIR = 'configure'
BASE_CONFIG_RAW_DATA = None
PORT = 8008
IPV4 = '0.0.0.0'

BASE_CONFIG_DATA: Dict

Collector.set('LISTEN', 'ipv4', IPV4)
Collector.set('LISTEN', 'port', PORT)

workspace_config = __import__('configure.AppConfig')
APP_ROOT = workspace_config.AppConfig.APP_ROOT
INSTALL_APP = workspace_config.AppConfig.INSTALL_APP
SETUP_MAIN_ROUTERS = workspace_config.AppConfig.SETUP_MAIN_ROUTERS

system_config = __import__('configure.SystemConfig')
COOKIE_SECRET = workspace_config.SystemConfig.COOKIE_SECRET
TEMPLATES_URL = workspace_config.SystemConfig.TEMPLATES_URL
STATIC_URL = workspace_config.SystemConfig.STATIC_URL
INDEX_FILE = workspace_config.SystemConfig.INDEX_FILE
BASE_DIR = workspace_config.SystemConfig.BASE_DIR


class _Setup(object):
    """
        配置框架所需的 端口，IP，日志等

    """

    def __init__(self):
        """

        :param base_config:
        """
        global BASE_DIR
        global LISTEN
        global BASE_CONFIG_RAW_DATA
        global BASE_CONFIG_FILE
        global BASE_CONFIG_DIR
        self.LISTEN = copy(LISTEN)
        self.BASE_DIR = copy(BASE_DIR)
        self.BASE_CONFIG_RAW_DATA = copy(BASE_CONFIG_RAW_DATA)
        self.BASE_CONFIG_FILE = copy(BASE_CONFIG_FILE)
        self.BASE_CONFIG_DIR = copy(BASE_CONFIG_DIR)

    def __resolve_base_config(self):

        self.BASE_CONFIG_FILE = self.base_config[0]
        if self.base_config.__len__() > 1:
            if issubclass(self.base_config[1], ConfigFileOperation):
                self.__base_config_handler = self.base_config[1]
            else:
                return ValueError("配置文件解析必须实现接口 ConfigFileOperation")

    def __load_base_data_config(self):
        self.BASE_CONFIG_RAW_DATA = self.__base_config_handler(
            os.path.join(self.BASE_DIR, self.BASE_CONFIG_DIR, self.BASE_CONFIG_FILE),
            Collector
        ).read()

    def __call__(self, base_config: Tuple[Union[str, ConfigFileOperation]]):
        self.base_config = base_config
        self.__base_config_handler = TomlConfigFileOperation
        self.__resolve_base_config()
        self.__load_base_data_config()


Setup = _Setup()
LISTEN = Collector.LISTEN

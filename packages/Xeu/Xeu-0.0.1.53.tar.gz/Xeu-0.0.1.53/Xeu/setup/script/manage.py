# _*_ coding:utf-8 _*_
import os
import sys
from colorama import init

from Xeu import Version
from Xeu.utils.DevConsole import StdoutColors
init(autoreset=True)


def create_workspace(workspace_name, current_path):
    workspace_path = os.path.join(current_path, workspace_name)
    print(f'{StdoutColors.OKGREEN}生成工作目录 -> {StdoutColors.ENDC}', workspace_path, f"{StdoutColors.OKGREEN}[OK]{StdoutColors.ENDC}")
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    return workspace_path


def create_configure(current_path):
    configure_path = os.path.join(current_path, 'configure')
    print(f'{StdoutColors.OKGREEN}生成配置文件 -> {StdoutColors.ENDC}', configure_path, f"{StdoutColors.OKGREEN}[OK]{StdoutColors.ENDC}")
    if not os.path.exists(configure_path):
        os.makedirs(configure_path)
    return configure_path


def create_log(current_path):
    configure_path = os.path.join(current_path, 'log')
    print(f'{StdoutColors.OKGREEN}生成日志目录 -> {StdoutColors.ENDC}', configure_path, f"{StdoutColors.OKGREEN}[OK]{StdoutColors.ENDC}")
    if not os.path.exists(configure_path):
        os.makedirs(configure_path)
    return configure_path


def create_configure_base___toml(configure_path):
    with open(os.path.join(configure_path, 'base.toml'), 'w', encoding="utf-8") as f:
        f.write("""# 环境
[runtime]
env='dev'

[listen]
    [listen.dev]
    ipv4 = '127.0.0.1'
    port = 8088""")


def create_configure__init___py(configure_path):
    with open(os.path.join(configure_path, '__init__.py'), 'w') as f:
        f.write("")


def create_configure_app_config_py(configure_path):
    with open(os.path.join(configure_path, 'AppConfig.py'), 'w', encoding="utf-8") as f:
        f.write("""# _*_ coding:utf-8 _*_

\"\"\"
    App loads the authentication record of the project
    The mapping of the main path of App
\"\"\"
from Xeu.core.route.RouterGroup import RouterGroup

\"\"\" App Register \"\"\"

INSTALL_APP = [
    'demo',
]

\"\"\"
    Prefix routing for App main routes、
\"\"\"

example_route_group = RouterGroup(
    group='example',
    route_map=dict(
        demo='demo1',
    )
)

SETUP_MAIN_ROUTERS = example_route_group.to_dict()

\"\"\"
    APP ROOT DIR
\"\"\"

APP_ROOT = 'app'

""")


def create_configure_system_config_py(configure_path):
    with open(os.path.join(configure_path, 'SystemConfig.py'), 'w', encoding="utf-8") as f:
        f.write("""# -*- coding: utf-8 -*-
import os


__all__ = [
    'EXPIRE_TIME_SECONDS', 'BASE_DIR', 'SET_DEFAULT_HEADER', 'COOKIE_SECRET',
    'TEMPLATES_URL', 'STATIC_URL', 'STATIC_URL_PREFIX', 'INDEX_FILE'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COOKIE_SECRET = 'ulb7bEIZmwpV545Z'
EXPIRE_TIME_SECONDS = 60 * 30


STATIC_RELATIVE = 'static'
STATIC_URL = os.path.join(BASE_DIR, STATIC_RELATIVE)
STATIC_URL_PREFIX_RAW = 'Front'
STATIC_URL_PREFIX = '/' + STATIC_URL_PREFIX_RAW + '/'
INDEX_FILE = "admin.html"
TEMPLATES_RELATIVE = 'templates'
TEMPLATES_URL = os.path.join(BASE_DIR, TEMPLATES_RELATIVE)


SET_DEFAULT_HEADER = {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
    "Access-Control-Allow-Methods": "POST, GET, PUT, PATCH",
    "Access-Control-Allow-Headers": "Origin,Content-Type,Accept,token,X-Requested-With"
}

\"\"\" 上传文件包存放路径 \"\"\"
UPLOAD_PACKAGE_URL = os.path.join(BASE_DIR, 'upload_package')
\"\"\" 上传 报告相关文件包 存放路径 \"\"\"
UPLOAD_REPORT_PACKAGE_URL = os.path.join(BASE_DIR, 'upload_package', 'report')

""")


def create_run(current_path):
    with open(os.path.join(current_path, 'run.py'), 'w', encoding="utf-8") as f:
        f.write("""#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from Xeu.core.loader.AppLoading import *
import tornado.ioloop
import tornado.httpserver


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(LISTEN.port, address=LISTEN.ipv4)
    http_server.start(1)
    Logger.info(f'[system] listen {LISTEN.ipv4} {LISTEN.port} ...')
    tornado.ioloop.IOLoop.instance().start()
""")


def create(workspace_name, current_path):
    _workspace_path = create_workspace(workspace_name, current_path)
    create_run(_workspace_path)
    create_app(_workspace_path)
    create_log(_workspace_path)
    _configure_path = create_configure(_workspace_path)
    create_configure_base___toml(_configure_path)
    create_configure__init___py(_configure_path)
    create_configure_app_config_py(_configure_path)
    create_configure_system_config_py(_configure_path)


def create_app(workspace_path):
    app_path = os.path.join(workspace_path, 'app')
    print(f'{StdoutColors.OKGREEN}生成App -> {StdoutColors.ENDC}', app_path, f"{StdoutColors.OKGREEN}[OK]{StdoutColors.ENDC}")
    if not os.path.exists(app_path):
        os.makedirs(app_path)
    with open(os.path.join(app_path, 'demo.py'), 'w', encoding="utf-8") as f:
        f.write("""# _*_ coding:utf-8 _*_
from Xeu.core.loader.ApplicationCore import *


@app.route(r'', name='Http Method Demo')
class HttpMethodDemoHandler(BaseHandlerCore):

    def initialize(self):
        Logger.info(f'{__class__} Ping pre...')

    @middleware()
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        Logger.info(f'{__class__} Ping ...')
        \"\"\"
        :desc 这是文档
        :param args:
        :param kwargs:
        :success return:
        \"\"\"
        try:
            self._res['data'] = "data_data_data"
            self._res['status'] = ResponseCode.InfoGothOK
            self.write(json.dumps(self._res))
            self.finish()
        except Exception as e:
            Logger.info(f'{__class__} Ping [Error] {str(e)}')
            self.write(json.dumps(dict(status=ResponseCode.ServicesError)))
            self.finish()


        """)


class Main(object):

    @staticmethod
    def init(workspace_name, current_path):
        create(workspace_name, current_path)

    @staticmethod
    def run(workspace_name, current_path):
        try:
            cmd = f"{sys.executable} {os.path.join(current_path, workspace_name, 'run.py')}"
            os.system(cmd)
        except Exception as e:
            print(f"{StdoutColors.FAIL}{e}{StdoutColors.ENDC}")

def run():
    main = Main()
    if sys.argv.__len__() == 3:
        getattr(main, sys.argv[1])(sys.argv[2], os.getcwd())
    else:
        getattr(main, sys.argv[1])(os.getcwd())


if __name__ == '__main__':
    # print(sys.argv)
    # print(os.getcwd())
    # print(sys.path[0])
    print("当前python：", sys.executable)
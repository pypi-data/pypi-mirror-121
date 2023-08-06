# _*_ coding:utf-8 _*_
import os
import sys


def create_workspace(workspace_name, current_path):
    workspace_path = os.path.join(current_path, workspace_name)
    print('create_workspace:', workspace_path)
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    return workspace_path


def create_configure(current_path):
    configure_path = os.path.join(current_path, 'configure')
    print('create_configure:', configure_path)
    if not os.path.exists(configure_path):
        os.makedirs(configure_path)
    return configure_path


def create_configure_base___toml(configure_path):
    with open(os.path.join(configure_path, 'base.toml'), 'w') as f:
        f.write(bytes("""# 环境
[runtime]
env='dev'

[listen]
    [listen.dev]
    ipv4 = '127.0.0.1'
    port = 8088"""))


def create_configure__init___py(configure_path):
    with open(os.path.join(configure_path, '__init__.py'), 'w') as f:
        f.write("")


def create(workspace_name, current_path):
    _workspace_path = create_workspace(workspace_name, current_path)
    create_app(_workspace_path)
    _configure_path = create_configure(current_path)
    create_configure_base___toml(_configure_path)
    create_configure__init___py(_configure_path)


def create_app(workspace_path):
    app_path = os.path.join(workspace_path, 'app')
    print('create_app:', app_path)
    if not os.path.exists(app_path):
        os.makedirs(app_path)
    with open(os.path.join(app_path, 'demo.py'), 'w') as f:
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


        """.encode('utf8'))


class Main(object):

    @staticmethod
    def init(workspace_name, current_path):
        create(workspace_name, current_path)


def run():
    main = Main()
    getattr(main, sys.argv[1])(sys.argv[2], os.getcwd())


if __name__ == '__main__':
    print(sys.argv)
    print(os.getcwd())
    print(sys.path[0])
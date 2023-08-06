# _*_ coding:utf-8 _*_
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_workspace(workspace_name):
    workspace_path = os.path.join(CURRENT_DIR, workspace_name)
    print('create_workspace:', workspace_path)
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    return workspace_path


def create(workspace_name):
    _workspace_path = create_workspace(workspace_name)
    create_app(_workspace_path)


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


        """)


class Main(object):

    @staticmethod
    def init(workspace_name):
        create(workspace_name)


def run():
    main = Main()
    getattr(main, sys.argv[1])(sys.argv[2])
    print('console 1', sys.argv[1])
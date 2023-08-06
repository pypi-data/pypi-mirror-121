# _*_ coding:utf-8 _*_
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app():
    app_path = os.path.join(CURRENT_DIR, 'app')
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
    def init():
        create_app()

    def get_args(self):
        getattr(self, sys.argv[1])()
        print('console 1', sys.argv[1])
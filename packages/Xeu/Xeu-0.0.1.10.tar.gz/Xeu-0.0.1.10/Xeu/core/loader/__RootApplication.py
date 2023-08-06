# _*_ coding:utf-8 _*_

"""
    故障问题的增删改查
"""
import tornado.web
import tornado.gen
import pymysql
import copy
import json

__all__ = ['BaseHandlerCore']


# class BaseHandlerCore(tornado.web.RequestHandler):
#
#     def __init__(self, application, request, **kwargs):
#         self.db_session = None
#         self.db_session_gen = None
#         self.apis = None
#         self._res = {'status': None}
#         super(BaseHandlerCore, self).__init__(application, request, **kwargs)
#
#     def initialize(self):
#
#         """ 初始化信息 """
#
#         Logger.info('[Executor] system [Run] 数据库连接...... ')
#         self.db_session_gen = SessionGen()
#         self.db_session_gen.run_engine()
#         self.db_session = self.db_session_gen.database_connects
#         Logger.info('[Executor] system [Run] 进入处理函数，并且初始化 [Status] 成功 ')
#
#     def on_finish(self):
#         # if self.db_session is not None:
#             try:
#                 self.db_session_gen.close()
#                 Logger.info('[Executor] system [Run]  断开数据库连接 [Status] 成功')
#
#             except Exception as e:
#                 Logger.info('[Executor] system [Run]  断开数据库连接 [Status] 失败 [Detail] %s' % str(e))


class BaseHandlerCore(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.service = None
        self._res = {'status': None}
        super(BaseHandlerCore, self).__init__(application, request, **kwargs)

    def initialize(self):

        """ 初始化信息 """

        pass

    def on_finish(self):
        pass

    def get_query_argument_json(self, params, default=None):
        __params = self.get_query_argument(params, default)
        if __params in [None, '']:
            return {}
        else:
            __res = json.loads(__params)
            return json.loads(__params)



# -*- coding: utf-8 -*-
from functools import wraps


def middleware(*middleware_args, **middleware_kwargs):
    # print(_func)
    # print(args)
    # print(middleware_kwargs)
    def _set_middleware(func):
        """
        中间件模块
        :param func:
        :return:
        """
        @wraps(func)
        def wrap(self, *args, **kwargs):
            """
            此处必须要有 *args, **kwargs 不然具名路由或者参数路由会出现问题
            :param self:
            :param args:
            :param kwargs:
            :return:
            """
            # 跨站域白名单

            import importlib
            # from Config.LoggingConf import Logger
            for middleware in middleware_args:
                _MiddlewaresSetup = importlib.import_module('Middlewares.'+middleware)
                _Middlewares = _MiddlewaresSetup.Core(_self=self, kwargs=kwargs)
                mid_res = _Middlewares.handle()
                if mid_res[0] is False:
                    self.write(mid_res[1])
                    self.finish()
                    return

            # _setting_headers = middleware_kwargs.get('set_header', SET_DEFAULT_HEADER)
            # if _setting_headers:
            #     for _setting, value in _setting_headers.items():
            #         self.set_header(_setting, value)
            try:
                # 管理端登录
                # Logger.info('method doc is %s' % func.__doc__)
                return func(self, *args, **kwargs)

            except Exception as e:
                # Logger.error('Service 执行 [状态] 失败 [详情] %s' % str(e))
                self.write('fail')
                self.finish()

        return wrap
    return _set_middleware
